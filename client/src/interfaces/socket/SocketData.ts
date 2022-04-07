
export default interface SocketData<T> {
    message: string,
    errors: string[],
    data: T
}