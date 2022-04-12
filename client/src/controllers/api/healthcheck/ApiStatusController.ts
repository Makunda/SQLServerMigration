/**
 * Manage the communication to retrieve Graph Communication
 */
import ProxyAxios from "../../../utils/api/ProxyAxios";
import Status from "../../../interfaces/healthcheck/status";

export default class ApiStatusController {

    /**
     * Get the status of the API
     */
    public async getStatus() : Promise<Status> {
        try {
            const data = await ProxyAxios.get<Status>("/status/")
            data.checkValidity();
            return data.getData()
        } catch (e) {
            return { status: false };
        }
    }
}