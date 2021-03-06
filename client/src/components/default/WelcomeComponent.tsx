import React from "react";
import Status from "../../interfaces/healthcheck/status";
import ApiStatusController from "../../controllers/api/healthcheck/ApiStatusController";


type CustomState = {
    isLoaded: boolean,
    status: Status,
    error: any
}

export class WelcomeComponent extends React.Component<{}, CustomState> {

    private statusController: ApiStatusController;

    constructor(props: any) {
        super(props);
        this.statusController = new ApiStatusController();

        this.state = {
            isLoaded: false,
            status: {} as Status,
            error: null
        }
    }

    async componentDidMount() {
        try {
            const status = await this.statusController.getStatus();
            const test = "Updated";

            this.setState({
                status: status
            })
        } catch (e) {
            this.setState({
                error: e
            })
        }
    }

    render() {

        return  (
            <div>
                <h3> The API is {this.state.status ? "Up" : "Down"}</h3>
            </div>
        )
    }
}