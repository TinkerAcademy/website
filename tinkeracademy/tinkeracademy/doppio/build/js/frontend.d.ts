/// <reference path="../../vendor/DefinitelyTyped/node/node.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/jquery/jquery.d.ts" />
/// <reference path="../../vendor/jquery.console.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/ace/ace.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/underscore/underscore.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/dropboxjs/dropboxjs.d.ts" />
/// <reference path="../../vendor/DefinitelyTyped/async/async.d.ts" />
declare var BrowserFS: {
    BFSRequire(name: 'process'): NodeJS.Process;
    BFSRequire(name: 'buffer'): {
        Buffer: typeof Buffer;
    };
    BFSRequire(name: string): any;
    FileSystem: any;
    initialize(fs: any): void;
};
declare var doppio: {
    javaCli: {
        java(args: string[], opts: any, cb: (arg: boolean) => void, startedCb?: (jvm: any) => void): void;
    };
};
interface FileReaderEvent extends ErrorEvent {
    target: FileReaderEventTarget;
}
interface FileReaderEventTarget extends EventTarget {
    files: File[];
    error: any;
}
interface TerminalCommand {
    getCommand(): string;
    getAutocompleteFilter(): (fname: string, isDir: boolean) => boolean;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
/**
 * Abstracts away the messiness of JQConsole.
 */
declare class Terminal {
    private _console;
    private _consoleElement;
    private _commands;
    constructor(consoleElement: JQuery, commands: TerminalCommand[], welcomeMessage: string);
    stdout(text: string): void;
    stderr(text: string): void;
    stdin(cb: (text: string) => void): void;
    runCommand(args: string[]): void;
    exitProgram(): void;
    getPromptText(): string;
    setPromptText(text: string): void;
    setPromptLabel(prompt: string): void;
    getAvailableCommands(): {
        [commandName: string]: TerminalCommand;
    };
    private _expandArguments(args, cb);
}
declare class AbstractTerminalCommand implements TerminalCommand {
    getCommand(): string;
    getAutocompleteFilter(): (fname: string, isDir: boolean) => boolean;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare var process: NodeJS.Process, Buffer: {
    new (str: string, encoding?: string): Buffer;
    new (size: number): Buffer;
    new (array: Uint8Array): Buffer;
    new (array: any[]): Buffer;
    new (buffer: Buffer): Buffer;
    prototype: Buffer;
    isBuffer(obj: any): obj is Buffer;
    isEncoding(encoding: string): boolean;
    byteLength(string: string, encoding?: string): number;
    concat(list: Buffer[], totalLength?: number): Buffer;
    compare(buf1: Buffer, buf2: Buffer): number;
}, fs: any, path: any, demoJars: string, demoClasses: string;
/**
 * Construct a JavaOptions object with the default demo fields filled in.
 * Optionally merge it with the custom arguments specified.
 */
declare function constructJavaOptions(customArgs?: {
    [prop: string]: any;
}): any;
/**
 * Maintain the size of the console.
 */
declare function onResize(): void;
declare function ps1(): string;
/**
 * Uploads the specified file via the FileReader interface. Calls the callback
 * with an optional error if one occurs.
 */
declare function uploadFile(f: File, cb: (e?: string) => void): void;
/**
 * Upload files via the browser's FileReader interface. Triggered when someone
 * clicks the upload button in the demo.
 */
declare function uploadFiles(terminal: Terminal, ev: FileReaderEvent): void;
declare function recursiveCopy(srcFolder: string, destFolder: string, cb: (err?: any) => void): void;
declare function copyFile(srcFile: string, destFile: string, cb: (err?: any) => void): void;
declare function pad_right(str: string, len: number): string;
declare function readDir(dir: string, pretty: boolean, columns: boolean, cb: (listing: string) => void): void;
declare function columnize(str_list: string[], line_length?: number): string;
declare class JavaCommand extends AbstractTerminalCommand {
    getCommand(): string;
    getAutocompleteFilter(): (fname: any, isDir: any) => boolean;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class JARCommand extends JavaCommand {
    private _cmd;
    private _jarPath;
    private _extraArgs;
    private _validExts;
    constructor(cmd: string, jarPath: string, extraArgs?: string[], validExts?: string[]);
    getCommand(): string;
    getAutocompleteFilter(): (fname: any, isDir: any) => boolean;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class JavaClassCommand extends JavaCommand {
    private _cmd;
    private _classpath;
    private _className;
    private _extraArgs;
    private _validExts;
    constructor(cmd: string, classpath: string, className: string, extraArgs?: string[], validExts?: string[]);
    getCommand(): string;
    getAutocompleteFilter(): (fname: any, isDir: any) => boolean;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class SimpleCommand extends AbstractTerminalCommand {
    private _command;
    private _runCommand;
    constructor(command: string, runCommand: (terminal: Terminal, args: string[], cb: () => void) => void);
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class LSCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class EditCommand extends AbstractTerminalCommand {
    private _consoleElement;
    private _filenameElement;
    private _editorContainer;
    private _saveButtonElement;
    private _closeButtonElement;
    private _editor;
    private _isInitialized;
    private _lastCb;
    constructor(editorElementName: string, saveButtonElement: JQuery, closeButtonElement: JQuery, editorContainer: JQuery, consoleElement: JQuery, filenameElement: JQuery);
    private initialize(terminal);
    private closeEditor();
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
    private defaultFile(filename);
}
declare class CatCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class MvCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class CpCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class MkdirCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class CDCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class RMCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class RmdirCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class MountDropboxCommand extends AbstractTerminalCommand {
    getCommand(): string;
    getAutocompleteFilter(): () => boolean;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class TimeCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class ProfileCommand extends AbstractTerminalCommand {
    getCommand(): string;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare class HelpCommand extends AbstractTerminalCommand {
    getCommand(): string;
    getAutocompleteFilter(): () => boolean;
    run(terminal: Terminal, args: string[], cb: () => void): void;
}
declare function tabComplete(terminal: Terminal, args: string[]): void;
declare function getCompletions(terminal: Terminal, args: string[], cb: (c: string[]) => void): void;
declare function filterSubstring(prefix: string, lst: string[]): string[];
declare function fileNameCompletions(cmd: string, args: string[], filter: (item: string, isDir: boolean) => boolean, cb: (c: string[]) => void): void;
declare function longestCommmonPrefix(lst: string[]): string;
/**
 * Calls `readdir` on each directory, and ignores any files in `dirs`.
 * Tests the result against the regular expression.
 * Passes back any directories that pass the test.
 */
declare function expandDirs(dirs: string[], r: RegExp, cb: (expansion: string[]) => void): void;
/**
 * Asynchronous method for processing a Unix glob.
 */
declare function processGlob(glob: string, cb: (expansion: string[]) => void): void;
