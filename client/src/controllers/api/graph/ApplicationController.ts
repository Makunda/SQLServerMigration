/**
 * Manage the communication to retrieve Graph Communication
 */
import ProxyAxios from "../../../utils/api/ProxyAxios";
import Status from "../../../interfaces/healthcheck/status";
import Logger from "../../../utils/logging/logger";

export default class ApplicationController {

    private baseRoute: string = "/application"
    private logger: Logger = Logger.getLogger("Application controller");

    /**
     * Build the route
     * @private
     */
    private buildRoute(route: string) {
        return this.baseRoute + route
    }

    /**
     * Get the list of application available on the Neo4j graph database
     */
    public async getApplicationList() : Promise<string[]> {
        try {
            const data = await ProxyAxios.get<string[]>(this.buildRoute("/list"))
            data.checkValidity();
            return data.getData()
        } catch (e) {
            this.logger.error("Failed to get the list of application", e);
            throw new Error("Failed to get the list of application.");
        }
    }
}