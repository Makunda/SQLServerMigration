import React from "react";
import {Grid} from "@mui/material";
import {ApplicationGraph} from "../graph/ApplicationGraph";
import ControlPanel from "../control/ControlPanel";


export default class MainView extends React.Component {
    render() {
        return (
            <Grid container spacing={2}>
                <Grid item xs={3}>
                    <ControlPanel></ControlPanel>
                </Grid>
                <Grid item xs={9}>
                    <ApplicationGraph></ApplicationGraph>
                </Grid>
            </Grid>
        )
    }
}