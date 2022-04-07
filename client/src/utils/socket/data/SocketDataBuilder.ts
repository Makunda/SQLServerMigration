import SocketImpl from "../SocketImpl";
import SocketDataImpl from "./SocketDataImpl";

export default class SocketDataBuilder<T> {

    private message: string = "";
    private errors: string[] = []

    private data: any = null;
    public dataType = null;

    /**
     * Set data
     * @param data
     */
    public setData(data: T) {
        this.data = data;
    }

    /**
     * Set one error
     * @param error Error to include
     */
    public setError(error: string) {
        this.errors.push(error);
    }

    /**
     * Set multiple errors
     * @param errors
     */
    public setErrors(errors: string[]) {
        this.errors = errors;
    }

    public build() : SocketDataImpl<T> {
        return new SocketDataImpl<T>(this.message, this.data, this.errors);
    }

    public constructor(message: string) {
        this.message = message;
    }

}