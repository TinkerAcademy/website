var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
/// <reference path="../../vendor/DefinitelyTyped/node/node.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/jquery/jquery.d.ts" />
/// <reference path="../../vendor/jquery.console.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/ace/ace.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/underscore/underscore.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/dropboxjs/dropboxjs.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/async/async.d.ts" />
/**
 * Abstracts away the messiness of JQConsole.
 */
var Terminal = (function () {
    function Terminal(consoleElement, commands, welcomeMessage) {
        var _this = this;
        this._console = null;
        this._commands = {};
        this._consoleElement = consoleElement;
        commands.forEach(function (c) {
            _this._commands[c.getCommand()] = c;
        });
        this._console = consoleElement.console({
            promptLabel: ps1(),
            commandHandle: function (line) {
                var parts = line.trim().split(/\s+/);
                _this.runCommand(parts);
                return null;
            },
            cancelHandle: function () {
                // XXX: Need a 'currentcommand' that I can cancel.
            },
            tabComplete: function () {
                // tabComplete;
                // tabComplete(terminal: Terminal, args: string[], filter: (item: string) => void): void {
                var promptText = _this._console.promptText(), args = promptText.split(/\s+/), cmd = _this._commands[args[0]];
                tabComplete(_this, args);
            },
            autofocus: false,
            animateScroll: true,
            promptHistory: true,
            welcomeMessage: welcomeMessage
        });
    }
    Terminal.prototype.showPrompt = function(text) {
        this._console.reprompt();
    }
    Terminal.prototype.stdout = function (text) {
        this._console.message(text, 'success', true);
    };
    Terminal.prototype.stderr = function (text) {
        this._console.message(text, 'error', true);
    };
    Terminal.prototype.stdin = function (cb) {
        var console = this._console, oldPrompt = console.promptLabel, oldHandle = console.commandHandle;
        console.promptLabel = '';
        // Reprompt with a temporary custom handler.
        console.reprompt();
        console.commandHandle = function (line) {
            console.commandHandle = oldHandle;
            console.promptLabel = oldPrompt;
            if (line === '\0') {
                // EOF
                cb(line);
            }
            else {
                line += "\n"; // so BufferedReader knows it has a full line
                cb(line);
            }
        };
    };
    Terminal.prototype.runCommand = function (args) {
        var _this = this;
        if (args[0] === '') {
            return this.exitProgram();
        }
        var command = this._commands[args[0]];
        if (command === undefined) {
            this.stderr("Unknown command " + args[0] + ". Type \"help\" for a list of commands.\n");
            this.exitProgram();
        }
        else {
            this._expandArguments(args.slice(1), function (expArgs, err) {
                if (err !== undefined) {
                    _this.stderr(command.getCommand() + ": " + err + "\n");
                    _this.exitProgram();
                }
                else {
                    command.run(_this, expArgs, function () {
                        _this.exitProgram();
                    });
                }
            });
        }
    };
    Terminal.prototype.exitProgram = function () {
        this._console.reprompt();
        this._consoleElement.click();
    };
    Terminal.prototype.getPromptText = function () {
        return this._console.promptText();
    };
    Terminal.prototype.setPromptText = function (text) {
        this._console.promptText(text);
    };
    Terminal.prototype.setPromptLabel = function (prompt) {
        this._console.promptLabel = prompt;
    };
    Terminal.prototype.getAvailableCommands = function () {
        return _.clone(this._commands);
    };
    Terminal.prototype._expandArguments = function (args, cb) {
        var expandedArgs = [];
        async.each(args, function (arg, cb) {
            if (arg.indexOf('*') == -1) {
                expandedArgs.push(arg);
                cb();
            }
            else {
                processGlob(arg, function (expansionTerms) {
                    if (expansionTerms.length > 0) {
                        expandedArgs = expandedArgs.concat(expansionTerms);
                        cb();
                    }
                    else {
                        cb(arg + ": No such file or directory");
                    }
                });
            }
        }, function (e) {
            cb(expandedArgs, e);
        });
    };
    return Terminal;
}());
var AbstractTerminalCommand = (function () {
    function AbstractTerminalCommand() {
    }
    AbstractTerminalCommand.prototype.getCommand = function () {
        throw new Error("Abstract method.");
    };
    AbstractTerminalCommand.prototype.getAutocompleteFilter = function () {
        return function (fname, isDir) { return true; };
    };
    AbstractTerminalCommand.prototype.run = function (terminal, args, cb) {
        throw new Error("Abstract method");
    };
    return AbstractTerminalCommand;
}());
var process = BrowserFS.BFSRequire('process'), Buffer = BrowserFS.BFSRequire('buffer').Buffer, fs = BrowserFS.BFSRequire('fs'), path = BrowserFS.BFSRequire('path'), demoJars = "/home/jars/", demoClasses = "/home/classes/";
/**
 * Construct a JavaOptions object with the default demo fields filled in.
 * Optionally merge it with the custom arguments specified.
 */
function constructJavaOptions(customArgs) {
    if (customArgs === void 0) { customArgs = {}; }
    return _.extend({
        bootstrapClasspath: ['resources.jar', 'rt.jar', 'jsse.jar', 'jce.jar', 'charsets.jar', 'jfr.jar', 'tools.jar'].map(function (item) { return "/sys/java_home/lib/" + item; }),
        classpath: [],
        javaHomePath: '/sys/java_home',
        extractionPath: '/jars',
        nativeClasspath: ['/sys/natives'],
        assertionsEnabled: false
    }, customArgs);
}
/**
 * Maintain the size of the console.
 */
function onResize() {
    var height = $(window).height() * 1;
    $('#console').height(height);
    $('#source').height(height);
}
// Returns prompt text, ala $PS1 in bash.
function ps1() {
    return process.cwd() + "$ ";
}
/**
 * Uploads the specified file via the FileReader interface. Calls the callback
 * with an optional error if one occurs.
 */
function uploadFile(f, cb) {
    var reader = new FileReader();
    reader.onerror = function (e) {
        switch (e.target.error.code) {
            case e.target.error.NOT_FOUND_ERR:
                return cb("File " + f.name + " not found.");
            case e.target.error.NOT_READABLE_ERR:
                return cb("File " + f.name + " is not readable.");
            case e.target.error.SECURITY_ERR:
                return cb("Cannot use the FileReader interface. You must launch your browser with --allow-file-access-from-files.");
        }
    };
    reader.onload = function (e) {
        fs.writeFile(process.cwd() + '/' + f.name, new Buffer(e.target.result), function (err) {
            if (err) {
                cb("" + err);
            }
            else {
                cb();
            }
        });
    };
    reader.readAsArrayBuffer(f);
}
/**
 * Upload files via the browser's FileReader interface. Triggered when someone
 * clicks the upload button in the demo.
 */
function uploadFiles(terminal, ev) {
    if (typeof FileReader === "undefined" || FileReader === null) {
        terminal.stderr("Your browser doesn't support file loading.\nTry using the editor to create files instead.\n");
        return terminal.exitProgram();
    }
    var fileCount = ev.target.files.length, filesUploaded = 0;
    if (fileCount > 0) {
        terminal.stdout("Uploading " + fileCount + " files...\n");
    }
    var files = ev.target.files;
    files.forEach(function (f) {
        uploadFile(f, function (e) {
            filesUploaded++;
            var str = "[" + filesUploaded + "/" + fileCount + "]: File " + f.name + " ";
            if (e) {
                str += "could not be saved: " + e + ".\n";
                terminal.stderr(str);
            }
            else {
                str += "successfully saved.\n";
                terminal.stdout(str);
            }
            if (filesUploaded === fileCount) {
                terminal.exitProgram();
            }
        });
    });
}
function recursiveCopy(srcFolder, destFolder, cb) {
    function processDir(srcFolder, destFolder, cb) {
        fs.mkdir(destFolder, function (err) {
            // Ignore EEXIST.
            if (err && err.code !== 'EEXIST') {
                cb(err);
            }
            else {
                fs.readdir(srcFolder, function (e, items) {
                    if (e) {
                        cb(e);
                    }
                    else {
                        async.each(items, function (item, next) {
                            var srcItem = path.resolve(srcFolder, item), destItem = path.resolve(destFolder, item);
                            fs.stat(srcItem, function (e, stat) {
                                if (e) {
                                    cb(e);
                                }
                                else {
                                    if (stat.isDirectory()) {
                                        processDir(srcItem, destItem, next);
                                    }
                                    else {
                                        copyFile(srcItem, destItem, next);
                                    }
                                }
                            });
                        }, cb);
                    }
                });
            }
        });
    }
    processDir(srcFolder, path.resolve(destFolder, path.basename(srcFolder)), cb);
}
function copyFile(srcFile, destFile, cb) {
    fs.readFile(srcFile, function (e, data) {
        if (e) {
            cb(e);
        }
        else {
            fs.writeFile(destFile, data, cb);
        }
    });
}
// TODO: Download file locally command.
$(window).resize(onResize);
$(document).ready(function () {
    // Set up initial size of the console.
    onResize();
    // Set up file system.
    var xhrfs = new BrowserFS.FileSystem.XmlHttpRequest('listings.json', 'tinkeracademy/doppio/build/demo_files/'), mfs = new BrowserFS.FileSystem.MountableFileSystem(), fs = BrowserFS.BFSRequire('fs');
    var tutorialsfs = new BrowserFS.FileSystem.XmlHttpRequest('tutorials.json', 'tinkeracademy/doppio/build/demo_files/tutorials/');
    mfs.mount('/sys', xhrfs);
    mfs.mount('/tutorials', tutorialsfs);
    BrowserFS.initialize(mfs);
    fs.mkdirSync('/mnt');
    mfs.mount('/mnt/localStorage', new BrowserFS.FileSystem.LocalStorage());
    fs.mkdirSync('/home');
    process.chdir('/home');
    recursiveCopy('/sys/classes', '/home', function (err) {
        recursiveCopy('/sys/jars', '/home', function (err) {
            recursiveCopy('/tutorials', '/home', function (err) {
                // Set up the master terminal object.
                fs.readFile("/sys/motd", function (e, data) {
                    var welcomeText = "";
                    if (!e) {
                        welcomeText = data.toString();
                    }
                    var terminal = new Terminal($('#console'), [
                        new JARCommand('ecj', demoJars + "ecj.jar", ['-Djdt.compiler.useSingleThread=true'], ['java']),
                        new JARCommand('rhino', demoJars + "rhino.jar", [], ['js']),
                        new JavaClassCommand('javac', demoClasses, "classes.util.Javac", [], ['java']),
                        new JavaClassCommand('javap', demoClasses, "classes.util.Javap", [], ['class']),
                        new JavaCommand(),
                        new LSCommand(),
                        new EditCommand('source', $('#save_btn'), $('#close_btn'), $('#ide'), $('#console'), $('#filename')),
                        new CatCommand(),
                        new MvCommand(),
                        new CpCommand(),
                        new MkdirCommand(),
                        new CDCommand(),
                        new RMCommand(),
                        new RmdirCommand(),
                        new MountDropboxCommand(),
                        new TimeCommand(),
                        new ProfileCommand(),
                        new HelpCommand()
                    ], welcomeText);
                    // set up the local file loaders
                    $('#file').change(function (ev) {
                        uploadFiles(terminal, ev);
                    });
                    // Set up stdout/stderr/stdin.
                    process.stdout.on('data', function (data) { return terminal.stdout(data.toString()); });
                    process.stderr.on('data', function (data) { return terminal.stderr(data.toString()); });
                    process.stdin.on('_read', function () {
                        terminal.stdin(function (text) {
                            // BrowserFS's stdin lets you write to it for emulation purposes.
                            process.stdin.write(new Buffer(text));
                        });
                    });
                    // Focus the terminal.
                    $('#console').click();
                    var tutorial = new Tutorial(fs, terminal);
                    tutorial.process("tutorial0");
                });
            });
        });
    });
});
function pad_right(str, len) {
    return str + Array(len - str.length + 1).join(' ');
}
// helper function for 'ls'
function readDir(dir, pretty, columns, cb) {
    fs.readdir(path.resolve(dir), function (err, contents) {
        if (err || contents.length == 0) {
            return cb('');
        }
        contents = contents.sort();
        if (!pretty) {
            return cb(contents.join('\n'));
        }
        var pretty_list = [];
        async.each(contents, 
        // runs on each element
        function (c, next_item) {
            fs.stat(dir + '/' + c, function (err, stat) {
                if (err == null) {
                    if (stat.isDirectory()) {
                        c += '/';
                    }
                    pretty_list.push(c);
                }
                next_item();
            });
        }, 
        // runs at the end of processing
        function () {
            if (columns)
                cb(columnize(pretty_list));
            else
                cb(pretty_list.join('\n'));
        });
    });
}
function columnize(str_list, line_length) {
    if (line_length === void 0) { line_length = 100; }
    var max_len = 0;
    for (var i = 0; i < str_list.length; i++) {
        var len = str_list[i].length;
        if (len > max_len) {
            max_len = len;
        }
    }
    var num_cols = (line_length / (max_len + 1)) | 0;
    var col_size = Math.ceil(str_list.length / num_cols);
    var column_list = [];
    for (var j = 1; j <= num_cols; j++) {
        column_list.push(str_list.splice(0, col_size));
    }
    function make_row(i) {
        return column_list.filter(function (col) { return col[i] != null; })
            .map(function (col) { return pad_right(col[i], max_len + 1); })
            .join('');
    }
    var row_list = [];
    for (var i = 0; i < col_size; i++) {
        row_list.push(make_row(i));
    }
    return row_list.join('\n');
}
// Set the origin location, if it's not already.
if (location['origin'] == null) {
    location['origin'] = location.protocol + "//" + location.host;
}
var JavaCommand = (function (_super) {
    __extends(JavaCommand, _super);
    function JavaCommand() {
        _super.apply(this, arguments);
    }
    JavaCommand.prototype.getCommand = function () {
        return "java";
    };
    JavaCommand.prototype.getAutocompleteFilter = function () {
        // complete all directories, and some files
        return function (fname, isDir) {
            if (isDir)
                return true;
            var dot = fname.lastIndexOf('.');
            var ext = dot === -1 ? '' : fname.slice(dot + 1);
            return ext === 'class' || ext === 'jar';
        };
    };
    JavaCommand.prototype.run = function (terminal, args, cb) {
        doppio.javaCli.java(args, constructJavaOptions({
            launcherName: this.getCommand()
        }), cb);
    };
    return JavaCommand;
}(AbstractTerminalCommand));
var JARCommand = (function (_super) {
    __extends(JARCommand, _super);
    function JARCommand(cmd, jarPath, extraArgs, validExts) {
        if (extraArgs === void 0) { extraArgs = []; }
        if (validExts === void 0) { validExts = []; }
        _super.call(this);
        this._cmd = cmd;
        this._jarPath = jarPath;
        this._extraArgs = extraArgs;
        this._validExts = validExts;
    }
    JARCommand.prototype.getCommand = function () {
        return this._cmd;
    };
    JARCommand.prototype.getAutocompleteFilter = function () {
        var _this = this;
        return function (fname, isDir) {
            if (isDir)
                return true;
            var dot = fname.lastIndexOf('.');
            var ext = dot === -1 ? '' : fname.slice(dot + 1);
            for (var i = 0; i < _this._validExts.length; i++) {
                if (ext === _this._validExts[i])
                    return true;
            }
            return false;
        };
    };
    JARCommand.prototype.run = function (terminal, args, cb) {
        var allArgs = ["-jar", this._jarPath].concat(this._extraArgs, args);
        _super.prototype.run.call(this, terminal, allArgs, cb);
    };
    return JARCommand;
}(JavaCommand));
var JavaClassCommand = (function (_super) {
    __extends(JavaClassCommand, _super);
    function JavaClassCommand(cmd, classpath, className, extraArgs, validExts) {
        if (extraArgs === void 0) { extraArgs = []; }
        if (validExts === void 0) { validExts = []; }
        _super.call(this);
        this._cmd = cmd;
        this._classpath = classpath;
        this._className = className;
        this._extraArgs = extraArgs;
        this._validExts = validExts;
    }
    JavaClassCommand.prototype.getCommand = function () {
        return this._cmd;
    };
    JavaClassCommand.prototype.getAutocompleteFilter = function () {
        var _this = this;
        return function (fname, isDir) {
            if (isDir)
                return true;
            var dot = fname.lastIndexOf('.');
            var ext = dot === -1 ? '' : fname.slice(dot + 1);
            for (var i = 0; i < _this._validExts.length; i++) {
                if (ext === _this._validExts[i])
                    return true;
            }
            return false;
        };
    };
    JavaClassCommand.prototype.run = function (terminal, args, cb) {
        var allArgs = ["-cp", (".:" + this._classpath), this._className].concat(this._extraArgs, args);
        _super.prototype.run.call(this, terminal, allArgs, cb);
    };
    return JavaClassCommand;
}(JavaCommand));
var SimpleCommand = (function (_super) {
    __extends(SimpleCommand, _super);
    function SimpleCommand(command, runCommand) {
        _super.call(this);
        this._command = command;
        this._runCommand = runCommand;
    }
    SimpleCommand.prototype.getCommand = function () {
        return this._command;
    };
    SimpleCommand.prototype.run = function (terminal, args, cb) {
        this._runCommand(terminal, args, cb);
    };
    return SimpleCommand;
}(AbstractTerminalCommand));
var LSCommand = (function (_super) {
    __extends(LSCommand, _super);
    function LSCommand() {
        _super.apply(this, arguments);
    }
    LSCommand.prototype.getCommand = function () {
        return 'ls';
    };
    LSCommand.prototype.run = function (terminal, args, cb) {
        if (args.length === 0) {
            readDir('.', true, true, function (listing) {
                terminal.stdout(listing + "\n");
                cb();
            });
        }
        else if (args.length === 1) {
            readDir(args[0], true, true, function (listing) {
                terminal.stdout(listing + "\n");
                cb();
            });
        }
        else {
            async.each(args, function (dir, next) {
                readDir(dir, true, true, function (listing) {
                    terminal.stdout(dir + ":\n" + listing + "\n\n");
                    next();
                });
            }, cb);
        }
    };
    return LSCommand;
}(AbstractTerminalCommand));
var EditCommand = (function (_super) {
    __extends(EditCommand, _super);
    function EditCommand(editorElementName, saveButtonElement, closeButtonElement, editorContainer, consoleElement, filenameElement) {
        _super.call(this);
        this._isInitialized = false;
        this._consoleElement = consoleElement;
        this._filenameElement = filenameElement;
        this._editorContainer = editorContainer;
        this._saveButtonElement = saveButtonElement;
        this._closeButtonElement = closeButtonElement;
        // Initiaize AceEdit.
        this._editor = ace.edit(editorElementName);
        this._editor.setTheme('ace/theme/twilight');
    }
    EditCommand.prototype.initialize = function (terminal) {
        var _this = this;
        if (!this._isInitialized) {
            this._isInitialized = true;
            this._saveButtonElement.click(function (e) {
                var fname = _this._filenameElement.val();
                var contents = _this._editor.getSession().getValue();
                if (contents[contents.length - 1] !== '\n') {
                    contents += '\n';
                }
                fs.writeFile(fname, contents, function (err) {
                    if (err) {
                        terminal.stderr("File could not be saved: " + err + "\n");
                    }
                    else {
                        terminal.stdout("File saved as '" + fname + "'.\n");
                    }
                    if (_this._lastCb != null) {
                        _this._lastCb();
                        _this._lastCb = null;
                    }
                });
                _this.closeEditor();
                e.preventDefault();
            });
            this._closeButtonElement.click(function (e) {
                _this.closeEditor();
                if (_this._lastCb != null) {
                    _this._lastCb();
                    _this._lastCb = null;
                }
                e.preventDefault();
            });
        }
    };
    EditCommand.prototype.closeEditor = function () {
        var _this = this;
        this._editorContainer.fadeOut('fast', function () {
            // click to restore focus
            _this._consoleElement.fadeIn('fast').click();
        });
    };
    EditCommand.prototype.getCommand = function () {
        return "edit";
    };
    EditCommand.prototype.run = function (terminal, args, cb) {
        var _this = this;
        this.initialize(terminal);
        var startEditor = function (data) {
            /*_this._consoleElement.fadeOut('fast', */(function () {
                _this._filenameElement.val(args[0]);
                _this._editorContainer.fadeIn('fast');
                if (args[0] == null || args[0].split('.')[1] === 'java') {
                    var JavaMode = ace.require("ace/mode/java").Mode;
                    _this._editor.getSession().setMode(new JavaMode);
                }
                else {
                    var TextMode = ace.require("ace/mode/text").Mode;
                    _this._editor.getSession().setMode(new TextMode);
                }
                _this._editor.getSession().setValue(data);
            })();/*);*/
        };
        if (args[0] == null) {
            startEditor(this.defaultFile('Test.java'));
            this._lastCb = cb;
        }
        else {
            fs.readFile(args[0], 'utf8', function (err, data) {
                if (err) {
                    startEditor(_this.defaultFile(args[0]));
                }
                else {
                    startEditor(data);
                }
                _this._lastCb = cb;
            });
        }
    };
    EditCommand.prototype.defaultFile = function (filename) {
        if (filename.indexOf('.java', filename.length - 5) != -1) {
            var lastSlash = filename.lastIndexOf('/');
            return "class " + filename.substring(lastSlash + 1, filename.length - 5) + " {\n  public static void main(String[] args) {\n    // enter code here\n  }\n}";
        }
        return "";
    };
    return EditCommand;
}(AbstractTerminalCommand));
var CatCommand = (function (_super) {
    __extends(CatCommand, _super);
    function CatCommand() {
        _super.apply(this, arguments);
    }
    CatCommand.prototype.getCommand = function () {
        return 'cat';
    };
    CatCommand.prototype.run = function (terminal, args, cb) {
        if (args.length == 0) {
            terminal.stdout("Usage: cat <file>\n");
            return cb();
        }
        async.eachSeries(args, function (item, next) {
            fs.readFile(item, 'utf8', function (err, data) {
                if (err) {
                    terminal.stderr("Could not open file '" + item + "': " + err + "\n");
                }
                else {
                    terminal.stdout(data);
                }
                next();
            });
        }, cb);
    };
    return CatCommand;
}(AbstractTerminalCommand));
var MvCommand = (function (_super) {
    __extends(MvCommand, _super);
    function MvCommand() {
        _super.apply(this, arguments);
    }
    MvCommand.prototype.getCommand = function () {
        return 'mv';
    };
    MvCommand.prototype.run = function (terminal, args, cb) {
        if (args.length < 2) {
            terminal.stdout("Usage: mv <from-file> <to-file>\n");
            return cb();
        }
        // TODO: support mv foo bar someDir/
        fs.rename(args[0], args[1], function (err) {
            if (err) {
                terminal.stderr("Could not rename " + args[0] + " to " + args[1] + ": " + err + "\n");
            }
            cb();
        });
    };
    return MvCommand;
}(AbstractTerminalCommand));
var CpCommand = (function (_super) {
    __extends(CpCommand, _super);
    function CpCommand() {
        _super.apply(this, arguments);
    }
    CpCommand.prototype.getCommand = function () {
        return 'cp';
    };
    CpCommand.prototype.run = function (terminal, args, cb) {
        if (args.length < 2) {
            terminal.stdout("Usage: cp <from-file> <to-file>\n");
            return cb();
        }
        var dest = args.pop();
        // hack around BFS bug: stat('foo/') fails for some reason
        if (dest.lastIndexOf('/') == dest.length - 1) {
            dest = dest.substr(0, dest.length - 1);
        }
        fs.stat(dest, function (err, stat) {
            if (err && err.code !== 'ENOENT') {
                terminal.stderr("Invalid destination: " + dest + ": " + err + "\n");
                cb();
            }
            else if (stat != null && stat.isDirectory()) {
                // copy args to dest directory
                async.each(args, function (item, next) {
                    copyFile(item, path.resolve(dest, path.basename(item)), function (err) {
                        if (err) {
                            terminal.stderr("Copy failed for " + item + ": " + err + "\n");
                        }
                        next();
                    });
                }, cb);
            }
            else if (args.length > 1) {
                terminal.stderr("Too many arguments for file target.\n");
                cb();
            }
            else if (args[0] == dest) {
                terminal.stderr("Source and target are identical.\n");
                cb();
            }
            else {
                copyFile(args[0], dest, function (err) {
                    if (err) {
                        terminal.stderr("Copy failed: " + err + "\n");
                    }
                    cb();
                });
            }
        });
    };
    return CpCommand;
}(AbstractTerminalCommand));
var MkdirCommand = (function (_super) {
    __extends(MkdirCommand, _super);
    function MkdirCommand() {
        _super.apply(this, arguments);
    }
    MkdirCommand.prototype.getCommand = function () {
        return 'mkdir';
    };
    MkdirCommand.prototype.run = function (terminal, args, cb) {
        if (args.length < 1) {
            terminal.stdout("Usage: mkdir <dirname>\n");
            return cb();
        }
        async.each(args, function (item, next) {
            fs.mkdir(item, function (err) {
                if (err) {
                    terminal.stderr("Could not make directory " + item + ": " + err + "\n");
                }
                next();
            });
        }, cb);
    };
    return MkdirCommand;
}(AbstractTerminalCommand));
var CDCommand = (function (_super) {
    __extends(CDCommand, _super);
    function CDCommand() {
        _super.apply(this, arguments);
    }
    CDCommand.prototype.getCommand = function () {
        return 'cd';
    };
    CDCommand.prototype.run = function (terminal, args, cb) {
        if (args.length > 1) {
            terminal.stdout("Usage: cd <directory>\n");
            cb();
        }
        else {
            var dir;
            if (args.length == 0 || args[0] == '~') {
                // Change to the default (starting) directory.
                dir = '/home';
            }
            else {
                dir = path.resolve(args[0]);
            }
            // Verify path exists before going there.
            // chdir does not verify that the directory exists.
            fs.exists(dir, function (doesExist) {
                if (doesExist) {
                    process.chdir(dir);
                    terminal.setPromptLabel(ps1());
                }
                else {
                    terminal.stderr("Directory " + dir + " does not exist.\n");
                }
                cb();
            });
        }
    };
    return CDCommand;
}(AbstractTerminalCommand));
var RMCommand = (function (_super) {
    __extends(RMCommand, _super);
    function RMCommand() {
        _super.apply(this, arguments);
    }
    RMCommand.prototype.getCommand = function () {
        return 'rm';
    };
    RMCommand.prototype.run = function (terminal, args, cb) {
        if (args[0] == null) {
            terminal.stdout("Usage: rm <file>\n");
            cb();
        }
        else {
            async.each(args, function (item, next) {
                fs.unlink(item, function (err) {
                    if (err) {
                        terminal.stderr("Could not remove file " + item + ": " + err + "\n");
                    }
                    next();
                });
            }, cb);
        }
    };
    return RMCommand;
}(AbstractTerminalCommand));
var RmdirCommand = (function (_super) {
    __extends(RmdirCommand, _super);
    function RmdirCommand() {
        _super.apply(this, arguments);
    }
    RmdirCommand.prototype.getCommand = function () {
        return 'rmdir';
    };
    RmdirCommand.prototype.run = function (terminal, args, cb) {
        if (args[0] == null) {
            terminal.stdout("Usage: rmdir <dir>\n");
            cb();
        }
        else {
            async.each(args, function (item, next) {
                fs.rmdir(item, function (err) {
                    if (err) {
                        terminal.stderr("Could not remove directory " + item + ": " + err + "\n");
                    }
                    next();
                });
            }, cb);
        }
    };
    return RmdirCommand;
}(AbstractTerminalCommand));
var MountDropboxCommand = (function (_super) {
    __extends(MountDropboxCommand, _super);
    function MountDropboxCommand() {
        _super.apply(this, arguments);
    }
    MountDropboxCommand.prototype.getCommand = function () {
        return 'mount_dropbox';
    };
    MountDropboxCommand.prototype.getAutocompleteFilter = function () {
        // takes no completable arguments
        return function () { return false; };
    };
    MountDropboxCommand.prototype.run = function (terminal, args, cb) {
        var api_key = "j07r6fxu4dyd08r";
        if (args.length < 1 || args[0] !== 'Y') {
            terminal.stdout("This command may redirect you to Dropbox's site for authentication.\nIf you would like to proceed with mounting Dropbox into the in-browser\nfilesystem, please type \"mount_dropbox Y\".\n\nOnce you have successfully authenticated with Dropbox and the page reloads,\nyou will need to type \"mount_dropbox Y\" again to finish mounting.\n(If you would like to use your own API key, please type \"mount_dropbox Y your_api_key_here\".)\n");
            cb();
        }
        else {
            if (args.length == 2 && args[1].length === 15) {
                api_key = args[1];
                terminal.stdout("Using API key " + api_key + "...\n");
            }
            var client = new Dropbox.Client({ key: api_key });
            client.authenticate(function (error, data) {
                var mfs;
                if (error == null) {
                    mfs = fs.getRootFS();
                    mfs.mount('/mnt/dropbox', new BrowserFS.FileSystem.Dropbox(client));
                    terminal.stdout("Successfully connected to your Dropbox account. You can now access files in the /Apps/DoppioJVM folder of your Dropbox account at /mnt/dropbox.\n");
                }
                else {
                    terminal.stderr("Unable to connect to Dropbox: " + error + "\n");
                }
                cb();
            });
        }
    };
    return MountDropboxCommand;
}(AbstractTerminalCommand));
var TimeCommand = (function (_super) {
    __extends(TimeCommand, _super);
    function TimeCommand() {
        _super.apply(this, arguments);
    }
    TimeCommand.prototype.getCommand = function () {
        return 'time';
    };
    TimeCommand.prototype.run = function (terminal, args, cb) {
        var command = args[0], commandObj = terminal.getAvailableCommands()[command];
        if (commandObj === undefined) {
            terminal.stderr("Undefined command: " + command + "\n");
            cb();
        }
        else {
            var start = (new Date).getTime();
            console.profile(command);
            commandObj.run(terminal, args.slice(1), function () {
                console.profileEnd();
                var end = (new Date).getTime();
                terminal.stdout("\nTime elapsed: " + (end - start) + " ms.\n");
                cb();
            });
        }
    };
    return TimeCommand;
}(AbstractTerminalCommand));
var ProfileCommand = (function (_super) {
    __extends(ProfileCommand, _super);
    function ProfileCommand() {
        _super.apply(this, arguments);
    }
    ProfileCommand.prototype.getCommand = function () {
        return 'profile';
    };
    ProfileCommand.prototype.run = function (terminal, args, cb) {
        var count = 0, runs = 5, duration = 0, command = args[0], commandObj = terminal.getAvailableCommands()[command];
        if (commandObj === undefined) {
            terminal.stdout("Undefined command: " + command + "\n");
            cb();
        }
        else {
            function timeOnce(isWarmup) {
                var start = (new Date).getTime();
                commandObj.run(terminal, args.slice(1), function () {
                    if (!isWarmup) {
                        var end = (new Date).getTime();
                        duration += end - start;
                    }
                    if (count < runs) {
                        timeOnce(false);
                    }
                    else {
                        terminal.stdout("\n" + command + " took an average of " + duration / runs + " ms to run.\n");
                        cb();
                    }
                });
            }
            timeOnce(true);
        }
    };
    return ProfileCommand;
}(AbstractTerminalCommand));
var HelpCommand = (function (_super) {
    __extends(HelpCommand, _super);
    function HelpCommand() {
        _super.apply(this, arguments);
    }
    HelpCommand.prototype.getCommand = function () {
        return 'help';
    };
    HelpCommand.prototype.getAutocompleteFilter = function () {
        // help command takes no arguments
        return function () { return false; };
    };
    HelpCommand.prototype.run = function (terminal, args, cb) {
        terminal.stdout("Ctrl-D is EOF.\n\n" +
            "Java-related commands:\n" +
            "  javac <source file>     -- Invoke the Java 6 compiler.\n" +
            "  java <class> [args...]  -- Run with command-line arguments.\n" +
            "  javap [args...] <class> -- Run the Java 6 disassembler.\n" +
            "  time                    -- Measure how long it takes to run a command.\n" +
            "  rhino                   -- Run Rhino, the Java-based JavaScript engine.\n\n" +
            "File management:\n" +
            "  cat <file>              -- Display a file in the console.\n" +
            "  edit <file>             -- Edit a file.\n" +
            "  ls <dir>                -- List files.\n" +
            "  mv <src> <dst>          -- Move / rename a file.\n" +
            "  rm <file>               -- Delete a file.\n" +
            "  mkdir <dir>             -- Create a directory.\n" +
            "  cd <dir>                -- Change current directory.\n" +
            "  mount_dropbox           -- Mount a Dropbox folder into the file system.\n\n");
        cb();
    };
    return HelpCommand;
}(AbstractTerminalCommand));
function tabComplete(terminal, args) {
    var promptText = terminal.getPromptText();
    var lastArg = _.last(args);
    getCompletions(terminal, args, function (completions) {
        if (completions.length == 1) {
            // only one choice: complete to it, then add a space (unless it's a directory)
            promptText = promptText.substr(0, promptText.length - lastArg.length);
            promptText += completions[0];
            if (promptText[promptText.length - 1] !== '/') {
                promptText += ' ';
            }
            terminal.setPromptText(promptText);
        }
        else if (completions.length > 0) {
            var prefix = longestCommmonPrefix(completions);
            if (prefix == '' || prefix == lastArg) {
                // We've no more sure completions to give, so show all options.
                var commonLen = lastArg.lastIndexOf('/') + 1;
                var options = completions.map(function (c) { return c.slice(commonLen); });
                options.sort();
                terminal.stdout(columnize(options) + "\n");
                terminal.exitProgram();
                terminal.setPromptText(promptText);
            }
            else {
                // Delete existing text so we can do case correction.
                promptText = promptText.substr(0, promptText.length - lastArg.length);
                terminal.setPromptText(promptText + prefix);
            }
        }
    });
}
function getCompletions(terminal, args, cb) {
    if (args.length == 1) {
        cb(filterSubstring(args[0], Object.keys(terminal.getAvailableCommands())));
    }
    else if (args[0] === 'time') {
        getCompletions(terminal, args.slice(1), cb);
    }
    else {
        var cmd = terminal.getAvailableCommands()[args[0]], filter = function () { return true; };
        if (cmd != null) {
            filter = cmd.getAutocompleteFilter();
        }
        fileNameCompletions(args[0], args, filter, cb);
    }
}
function filterSubstring(prefix, lst) {
    return lst.filter(function (x) { return x.substr(0, prefix.length) == prefix; });
}
function fileNameCompletions(cmd, args, filter, cb) {
    var toComplete = _.last(args);
    var lastSlash = toComplete.lastIndexOf('/');
    var dirPfx, searchPfx;
    if (lastSlash >= 0) {
        dirPfx = toComplete.slice(0, lastSlash + 1);
        searchPfx = toComplete.slice(lastSlash + 1);
    }
    else {
        dirPfx = '';
        searchPfx = toComplete;
    }
    var dirPath = (dirPfx == '') ? '.' : path.resolve(dirPfx);
    fs.readdir(dirPath, function (err, dirList) {
        var completions = [];
        if (err != null) {
            return cb(completions);
        }
        dirList = filterSubstring(searchPfx, dirList);
        async.each(dirList, 
        // runs on each element
        function (item, next) {
            fs.stat(path.resolve(dirPfx + item), function (err, stats) {
                if (err != null) {
                }
                else if (stats.isDirectory() && filter(item, true)) {
                    completions.push(dirPfx + item + '/');
                }
                else if (filter(item, false)) {
                    completions.push(dirPfx + item);
                }
                next();
            });
        }, 
        // runs at the end of processing
        function () { return cb(completions); });
    });
}
// use the awesome greedy regex hack, from http://stackoverflow.com/a/1922153/10601
function longestCommmonPrefix(lst) {
    return lst.join(' ').match(/^(\S*)\S*(?: \1\S*)*$/i)[1];
}
/**
 * Calls `readdir` on each directory, and ignores any files in `dirs`.
 * Tests the result against the regular expression.
 * Passes back any directories that pass the test.
 */
function expandDirs(dirs, r, cb) {
    var expanded = [];
    async.each(dirs, function (dir, next_item) {
        fs.readdir(dir, function (err, contents) {
            var i;
            if (err == null) {
                for (i = 0; i < contents.length; i++) {
                    if (r.test(contents[i])) {
                        // Note: We don't 'resolve' because we don't want the path to become
                        // absolute if it was relative in the first place.
                        expanded.push(path.join(dir, contents[i]));
                    }
                }
            }
            next_item();
        });
    }, function () {
        cb(expanded);
    });
}
/**
 * Asynchronous method for processing a Unix glob.
 */
function processGlob(glob, cb) {
    var globNormalized = path.normalize(glob), pathComps = globNormalized.split('/'), 
    // We bootstrap the algorithm with '/' or '.', depending on whether or not
    // the glob is a relative or absolute path.
    expanded = [glob.charAt(0) === '/' ? '/' : '.'];
    /**
     * Constructs a regular expression for a given glob pattern.
     */
    function constructRegExp(pattern) {
        return new RegExp("^" + pattern.replace(/\./g, "\\.").split('*').join('[^/]*') + "$");
    }
    // Process each component of the path separately.
    async.eachSeries(pathComps, function (path_comp, next_item) {
        var r;
        if (path_comp === "") {
            // This condition occurs for:
            // * The first component in an absolute directory.
            // * The last component in a path that ends in '/' (normalize doesn't remove it).
            return next_item();
        }
        r = constructRegExp(path_comp);
        expandDirs(expanded, r, function (_expanded) {
            expanded = _expanded;
            next_item();
        });
    }, function (e) {
        cb(expanded);
    });
}
//# sourceMappingURL=frontend.js.map