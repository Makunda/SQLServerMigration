
import SocketData from "../../../interfaces/socket/SocketData";

/**
 * Socket Data
 */
export default class SocketDataImpl<T> implements SocketData<T> {
    data: T;
    errors: string[];
    message: string;

    constructor(message: string, data: T, errors: string[]){
        this.message = message;
        this.data = data;
        this.errors = errors;
    }
}