import QtQuick
import Quickshell.Io

// One agent's usage record. FileView only watches; the bytes are read through
// the bounded no-follow helper so a planted symlink, FIFO, or huge file never
// lands in the long-lived shell.
Item {
  id: root
  visible: false

  property string agentId: ""
  property string path: ""
  property string reader: ""
  property var record: null
  readonly property int maxRecordChars: 256 * 1024

  property string _buf: ""
  property bool _overflow: false
  property bool _reloadPending: false
  property int _loadGen: 0

  FileView {
    path: root.path
    watchChanges: true
    preload: false
    printErrors: false
    onFileChanged: root.reloadBounded()
  }

  Process {
    id: readProc
    running: false
    property int job: 0
    stdout: SplitParser {
      splitMarker: ""
      onRead: function(chunk) {
        if (readProc.job !== root._loadGen || root._overflow) return
        var piece = String(chunk || "")
        if (root._buf.length + piece.length > root.maxRecordChars) {
          root._overflow = true
          readProc.running = false
          return
        }
        root._buf += piece
      }
    }
    onExited: {
      if (readProc.job !== root._loadGen) return
      if (root._overflow) {
        // Keep the last valid snapshot visible if a replacement is being
        // written or the bounded read cannot complete. The next file-change
        // event will retry and replace it when a complete record is ready.
        root.finishPendingReload()
        return
      }
      root.parse(root._buf)
      root.finishPendingReload()
    }
  }

  Component.onCompleted: root.reloadBounded()
  onPathChanged: root.reloadBounded()
  onReaderChanged: root.reloadBounded()

  function reloadBounded() {
    if (root.reader === "" || root.path === "" || root.agentId === "") {
      root.record = null
      return
    }
    // Several atomic record replacements can arrive close together. Let the
    // active bounded read finish, then do one more read; killing and replacing
    // a Process here can make its old onExited handler see the new job id and
    // parse a partial stdout buffer as a record.
    if (readProc.running) {
      root._reloadPending = true
      return
    }
    root._loadGen++
    root._buf = ""
    root._overflow = false
    readProc.job = root._loadGen
    readProc.command = ["python3", "-B", root.reader, "--load-json", root.path]
    readProc.running = true
  }

  function finishPendingReload() {
    if (!root._reloadPending) return
    root._reloadPending = false
    Qt.callLater(function() { root.reloadBounded() })
  }

  function parse(content) {
    try {
      var parsed = JSON.parse(String(content || ""))
      var record = parsed && parsed.ok === true ? parsed.record : null
      if (!record || typeof record !== "object") {
        // Treat missing, partial, and unreadable snapshots as a failed refresh,
        // not as an instruction to erase the last good display data.
        return
      }
      var id = String(record.id || "")
      if (id !== root.agentId) record.id = root.agentId
      // Codex may successfully refresh local usage while its optional limits
      // RPC returns an empty list. Keep the last fetched windows until a later
      // successful limits response replaces them.
      if (root.agentId === "codex" && Array.isArray(record.limits)
          && record.limits.length === 0 && root.record
          && Array.isArray(root.record.limits) && root.record.limits.length > 0) {
        record.limits = root.record.limits
        if (!record.tierLabel) record.tierLabel = root.record.tierLabel || ""
      }
      root.record = record
    } catch (e) {
      console.warn("agents", "Ignoring bad usage record", root.path, e)
    }
  }
}
