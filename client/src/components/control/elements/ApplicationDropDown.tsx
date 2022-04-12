import React from "react";
import ApplicationController from "../../../controllers/api/graph/ApplicationController";
import { useSelector, useDispatch } from 'react-redux'
import {FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from "@mui/material";
import { changeApplication } from '../../../store/features/ApplicationSlice'


export default class ApplicationDropDown extends React.Component {

    private applicationController: ApplicationController;

    public state: any = {
        applicationList: [] as string[],
        selectedApplication: "",
        error: {} as any
    }

    /**
     * Get the list of application
     * @private
     */
    private async getApplicationList() {
        try {
            const applicationList = await this.applicationController.getApplicationList();
            this.setState({
                applicationList: applicationList,
                selectedApplication: applicationList.length > 0 ? applicationList[0] : "",
                error: {}
            })
        } catch (e) {
            this.setState({
                applicationList: [],
                selectedApplication: "",
                error: e
            });
        }
    }

    /**
     * Handle the application change in the drop down
     * @param event
     * @private
     */
    private handleChange = (event: SelectChangeEvent) =>  {
        const selectedApplication = event.target.value as string;
        this.props.dispatch(changeApplication(selectedApplication))
    };

    componentDidMount() {
        this.getApplicationList();
    }

    constructor(props: any) {
        super(props);
        this.applicationController = new ApplicationController();
    }

    render() {
        return (
            <FormControl variant="filled" color={ "primary"} fullWidth>
                <InputLabel id="demo-simple-select-label">Application</InputLabel>
                <Select
                    labelId="application-dropdown-list"
                    id="application-dropdown-list"
                    value={this.state.selectedApplication || ''}
                    label="Application"
                    onChange={this.handleChange}
                >
                    {this.state.applicationList.map((x: string) => {
                        const value = x || "";
                        return (
                            <MenuItem key={value} value={value}>{value}</MenuItem>
                        )
                    })}
                </Select>
            </FormControl>
        )
    }
}