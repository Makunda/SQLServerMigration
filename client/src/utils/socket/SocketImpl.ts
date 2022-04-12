import {io, Socket} from "socket.io-client";
import SocketData from "../../interfaces/socket/SocketData";
import Logger from "../logging/logger";

// Call back type
type socketCallBack = (...args: any[]) => void
type responseCallBack = (...args: any[]) => SocketData<any>

/**
 * Wrapper of the Socket IO Class
 */
export default class  SocketImpl {

    private socket: Socket<any, any>;
    private namespace: string;
    private logger: Logger = Logger.getLogger("Socket Implementation");

    /**
     * Declare an action when receiving a message
     * @param message
     * @param callback
     */
    public on(message: string, callback: socketCallBack) : SocketImpl {
        this.socket.on(message, (data: any) => {
            this.logger.info(`Socket response for event: '${message}'. Data:`, data)
            callback(data);
        })
        return this;
    }

    /**
     * Synchronized on message
     * @param message Message to wait for
     */
    public async syncOn<T>(message: string) : Promise<SocketData<T>> {
        return new Promise(((resolve, reject) => {
            // On message redirect to resolve
            this.socket.on(message, (message: any) => {
                resolve(message as SocketData<T>);
            })

            // Reject if failed
            this.socket.on("error", (message: any) => {
                reject(message as SocketData<T>);
            })
        }))
    }

    /**
     * Disconnect the socket from the endpoint
     */
    public disconnect() : SocketImpl {
        this.socket.disconnect()
        return this;
    }

    private toString<T>(data: SocketData<T>) {
        return JSON.stringify(data);
    }

    /**
     * Emit a message on the current socket
     * @param message Message to send
     * @param data Data to pass
     * @param callback
     */
    public emit<T>(message: string, data: SocketData<T>, callback: socketCallBack | null = null) : SocketImpl {
        this.logger.info(`Emitting on '${this.namespace}'. Message: '${message}'. Data:`, data);

        if(callback == null ) this.socket.emit(message, data);
        else this.socket.emit(message, data, callback);

        return this;
    }

    /**
     * Refresh the connection of the socket
     */
    public refresh() : SocketImpl {
        if(!this.socket.active) {
           this.socket.connect()
        }

        return this
    }

    /**
     * Open the socket
     */
    public open() {
        this.socket.open();
    }

    /**
     * Get the status of the Socket
     */
    public getStatus() : boolean {
        return this.socket.active;
    }

    /**
     * Constructor
     * @param namespace Namespace to use
     * @param parameters
     */
    public constructor(namespace: string, parameters: any = null) {
        if(parameters == null) parameters = {};
        this.namespace = namespace;

        this.logger.info(`Building new socket for ${namespace}.`)
        this.socket = io(namespace, {
            auth: {
                'test': 'test'
            }});
    }
}