export default class ApiError extends Error {
    constructor(method: string, route: string, status: number, errors?: string[]) {
        super(`Failed to '${method}' resource at '${route}' [Status = ${status}]. ${ (errors && errors.length > 0) ? `Errors: ${Array.of(errors).join(", ")}` : '' }`);
    }
}