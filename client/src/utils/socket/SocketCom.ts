import SocketImpl from "./SocketImpl";
import {Runtime} from "inspector";

/**
 * Centralized socket manager
 */
export default class SocketCom {

    private static INSTANCE: SocketCom;
    private socketMap: Map<string, SocketImpl>;

    /**
     * Get the base url
     */
    public static getBaseUrl(): string {
        return `ws://localhost`;
    }

    /**
     * Open a new socket
     * @param namespace Namespace of the room to open
     * @param parameters (Optional) Authentication process
     */
    public openSocket(namespace: string, parameters: any = null) : SocketImpl {
        const socketUrl = SocketCom.getBaseUrl() + namespace;

        // Create a new socket
        if(!this.socketMap.has(socketUrl)) {
            this.socketMap.set(socketUrl, new SocketImpl(socketUrl, parameters));
        }

        // Get the socket and refresh if found
        const sock: SocketImpl | undefined =  this.socketMap.get(socketUrl);
        if(typeof sock == "undefined") throw new Error(`Failed to open a new Socket (url: ${socketUrl})`)

        sock.refresh();
        return sock;
    }

    /**
     * Singleton private constructor
     */
    private constructor() {
        this.socketMap = new Map<string, SocketImpl>();
    }

    /**
     * Get the instance of the Socket Communication layer
     */
    public static getInstance() : SocketCom {
        if( this.INSTANCE == null) this.INSTANCE = new SocketCom();
        return this.INSTANCE;
    }

    public static getSocket(namespace: string, parameters: any = null) : SocketImpl {
        const comSock = this.getInstance();
        return comSock.openSocket(namespace, parameters);
    }

}