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
    public setData(data: T) : SocketDataBuilder<T>{
        this.data = data;
        return this;
    }

    /**
     * Set one error
     * @param error Error to include
     */
    public setError(error: string) : SocketDataBuilder<T> {
        this.errors.push(error);
        return this;
    }

    /**
     * Set multiple errors
     * @param errors
     */
    public setErrors(errors: string[]): SocketDataBuilder<T> {
        this.errors = errors;
        return this;
    }

    public build() : SocketDataImpl<T> {
        return new SocketDataImpl<T>(this.message, this.data, this.errors);
    }

    public constructor(message: string) {
        this.message = message;
    }

}