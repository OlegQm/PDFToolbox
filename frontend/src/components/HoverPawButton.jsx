import React from "react";
import { useRive } from "@rive-app/react-canvas";
import pawRiv from "../components/PawButton.riv";

export default function HoverPawButton({ children, ...props }) {
    const { rive, RiveComponent } = useRive({
        src: pawRiv,
        animations: "Timeline 1",
        autoplay: false,
    });



    const handleEnter = () => rive && rive.play("Timeline 1");
    const handleLeave = () => rive && rive.pause();

    return (
        <div
            onMouseEnter={handleEnter}
            onMouseLeave={handleLeave}
            {...props}
            style={{ position: "relative", display: "inline-block" }}
        >
            <button>{children}</button>
            <RiveComponent
                style={{
                    position: "absolute",
                    bottom: 0,
                    right: "100%",
                    width: "80px",
                    pointerEvents: "none",
                }}
            />
        </div>
    );
}
