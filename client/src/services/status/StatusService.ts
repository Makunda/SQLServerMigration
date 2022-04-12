import {Status} from "../../enum/status/Status";
import Logger from "../../utils/logging/logger";
import ApiStatusController from "../../controllers/api/healthcheck/ApiStatusController";
import WebSocketStatusController from "../../controllers/socket/healthcheck/WebSocketStatusController";

/**
 * Service handling the status of the different major components
 */
export default class StatusService {

    private static INSTANCE: StatusService;

    // Utils
    private logger : Logger = Logger.getLogger("Status Service");

    // Service
    private apiStatusController = new ApiStatusController();
    private websocketController = new WebSocketStatusController();

    // Status
    private webSocketStatus: Status = Status.UNKNOWN;
    private webApiStatus: Status = Status.UNKNOWN;
    private neo4jStatus: Status = Status.UNKNOWN;

    public initialization() {
        this.getWebApiStatus().then().catch(err => {
            this.logger.error("Failed to verify the status of the Web API.", err);
        });
        this.getWebSocketStatus().then().catch(err => {
            this.logger.error("Failed to verify the status of the Web Socket.", err);
        });;
    }

    /**
     * Get the Web Api Status
     * @private
     */
    private async getWebApiStatus() {
        try {
            if(await this.apiStatusController.getStatus()) {
                this.webApiStatus = Status.UP;
                this.logger.info("The Server Web API is up.")
            } else {
                this.webApiStatus = Status.DOWN;
                this.logger.info("The Server Web API is down.")
            }
        } catch (e) {
            this.logger.error("Failed to get the Web API Status.", e);
            this.webApiStatus = Status.DOWN;
        }
    }

    /**
     * Get the Web socket
     * @private
     */
    private async getWebSocketStatus() {
        try {
            if(await this.websocketController.getStatus()) {
                this.webApiStatus = Status.UP;
                this.logger.info("The Server Web Socket is up.")
            } else {
                this.webApiStatus = Status.DOWN;
                this.logger.info("The Server Web Socket is down.")
            }
            this.webSocketStatus = Status.UP;
        } catch (e) {
            this.logger.error("Failed to get the Web Socket Status.", e);
            this.webApiStatus = Status.DOWN;
        }
    }

    private constructor() {

    }

    /**
     * Get the instance of the Status Service
     */
    public static getInstance() : StatusService {
        if(this.INSTANCE == null) this.INSTANCE = new StatusService();
        return this.INSTANCE;
    }


}