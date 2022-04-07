import {AxiosRequestConfig, AxiosResponse} from "axios";
import {ApiResponse} from "./ApiResponse";
import ApiError from "../../../errors/api/ApiError";

/** *
 * Class handling the response from the API
 */
export default class ApiResponseImpl<T> {
    private message = "";

    private status: number;

    private config: AxiosRequestConfig;

    private data: T = {} as any;

    private response = {} as ApiResponse;

    private errors: string[] = [];

    private success: boolean;

    /**
     * Create a Response from  a successful request
     * @param response Axios response
     */
    constructor(response: AxiosResponse) {
        this.status = response.status;
        this.config = response.config;

        if (!response.data) {
            this.success = false;
            this.errors = [`Request failed with status : ${response.status}.`];
        } else {
            // Response contains data; check for errors
            this.response = response.data as ApiResponse;


            this.message = response.data.message;
            this.errors = response.data.errors || [];

            if (this.errors.length > 0) {
                this.success = false;
            } else {
                this.success = true;
                this.data = (response.data.data || {}) as T;
            }
        }
    }

    /**
     * Check if the API response is positive or not
     * @returns True if the query was successfully executed
     */
    public isSuccess(): boolean {
        return this.success;
    }

    public isError(): boolean {
        return !this.success;
    }

    /**
     * Get the status
     * @returns The status of the response
     */
    public getStatus(): number {
        return this.status;
    }

    /**
     * Throw an Exception if the request failed
     */
    public checkValidity() {
        if(this.isError()) {
            const method = this.config.method as string || "Unknown"
            const url = this.config.url as string || "Unknown"
            throw new ApiError(method, url, this.status, this.errors)
        }
        // Else pass
    }

    /**
     * Is the status of the request successful
     */
    public isStatusSuccess(): boolean {
        const toStringStatus = String(this.status);
        return toStringStatus.startsWith("2") || toStringStatus.startsWith("3");
    }

    /**
     *
     * @returns Data of the response
     */
    public getData(): T {
        return this.data;
    }

    /**
     * Get the config of the request
     */
    public getConfiguration(): any {
        return this.config;
    }

    /**
     * Get the response from the API
     * @returns The raw response
     */
    public getRawResponse(): ApiResponse {
        return this.response;
    }

    /**
     * Get the list of the errors
     * @returns List of errors from the API
     */
    public getErrors(): string[] {
        return this.errors;
    }

    /**
     * The list of errors as a string
     * @param joiner (Optional) The string to join the elements. By default ", "
     * @returns The list of errors joined
     */
    public getErrorsAsString(joiner = ", "): string {
        return this.errors.join(joiner);
    }

    public getMessage(): string {
        return this.message;
    }
}
