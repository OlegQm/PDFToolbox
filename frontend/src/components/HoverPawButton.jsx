import React from "react";
import { useRive, Layout, Fit, Alignment } from "@rive-app/react-canvas";
import pawRiv from "../components/6.riv";
import "../components/HoverPawButton.css";
export default function HoverPawButton({ children, className, disabled, ...props }) {
    const { rive, RiveComponent } = useRive({
        src: pawRiv,
        animations: "Timeline 1",
        autoplay: false,
        layout: new Layout({
            fit:     Fit.Cover,        // Try Fit.Fill if you don’t mind cropping
            alignment: Alignment.Center
        }),
    });


    const handleEnter = () => rive && rive.play("Timeline 1");
    const handleLeave = () => rive && rive.pause();

    return (
        <div
            className="paw-button-wrapper"
            onMouseEnter={handleEnter}
            onMouseLeave={handleLeave}
            style={{ position: "relative", display: "inline-block" }}
        >
            <button
                className={className}
                disabled={disabled}
                {...props}
            >
                {children}
            </button>
            <RiveComponent className="paw-rive" />


        </div>
    );
}
