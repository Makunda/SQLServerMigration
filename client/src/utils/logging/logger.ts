
export default class Logger {

    private readonly name: string = "";

    private getTimestamp(): string {
        return new Date().toISOString();
    }

    /**
     * Format the message with a standard format
     * @param level Level of the logging
     * @param message Message to send
     * @private
     */
    private formatMessage(level: string, message: string) {
        return `${level.toUpperCase()} :: ${this.name} :: ${this.getTimestamp()} :: ${message}`;
    }

    public info(message: string, ...data: any): void {
        if(!data || data === []) console.log(this.formatMessage("INFO", message));
        else console.log(this.formatMessage("INFO", message), data);
    }

    public error(message: string, error: any) : void {
        console.error(this.formatMessage("ERROR", message), error);
    }

    public warn(message: string, ...data: any): void {
        console.warn(this.formatMessage("WARN", message), data)
    }

    /**
     * Private constructor for named Logger
     * @param name Name of the logger
     * @private
     */
    private constructor(name: string) {
        this.name = name;
    }

    /**
     * Get a logger
     * @param name
     */
    public static getLogger(name: string) : Logger {
        return new Logger(name);
    }

}