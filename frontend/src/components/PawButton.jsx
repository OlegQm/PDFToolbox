import React, { useRef } from "react";
import "./PawButton.css";
import padNoClaws   from "./paw_pad.png";
import padClaws     from "./paw_pad_claws.png";
import topClaws     from "./paw_top_claws.png";

export default function PawButton({ children, ...props }) {
    const pawRef  = useRef();
    const baseRef = useRef();

    function start() {
        const paw  = pawRef.current;
        const base = baseRef.current;

        base.style.display      = "block";
        base.className         = "paw-base paw-base--emerge";

        paw.src                 = padNoClaws;
        paw.style.display       = "block";
        paw.className           = "paw paw--emerge";
    }

    function handleMouseEnter() {
        const base = baseRef.current;
        const paw  = pawRef.current;

        base.style.display   = "block";
        base.className       = "paw-base paw-base--emerge";

        paw.style.display    = "block";
        paw.className        = "paw paw--emerge";
    }

    function handleAnimationEnd(e) {
        const base = baseRef.current;
        const paw  = pawRef.current;

        switch (e.animationName) {
            case "emerge":
                paw.src       = padClaws;            // добавить когти
                paw.className = "paw paw--fall";
                break;
            case "fall":
                paw.src       = topClaws;            // тыльная сторона
                paw.className = "paw paw--scratch";
                break;
            case "scratch":
                paw.className = "paw paw--retract";
                break;
            case "retract":
                paw.style.display    = "none";
                paw.className        = "paw";
                base.className       = "paw-base paw-base--retract";
                base.addEventListener("animationend", () => {
                    base.style.display = "none";
                }, { once: true });
                break;
            default:
                break;
        }
    }


    return (
        <div className="paw-button-wrapper">
            <button
                {...props}
                onMouseEnter={handleMouseEnter}
                onAnimationEnd={handleAnimationEnd}
            >
                {children}
            </button>

            <div ref={baseRef} className="paw-base">
                {/* Лапа — внутри основания */}
                <img
                    ref={pawRef}
                    className="paw"
                    alt="cat paw"
                    onAnimationEnd={handleAnimationEnd}
                />
            </div>
        </div>
    );
}
