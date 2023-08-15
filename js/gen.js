const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');
const Vex = require('vexflow');

const main = () => {
    // intervals
    const MAIN_INTERVALS = [4, 5];
    const EXTRA_INTERVALS = [1, 1, 1, 2, 2, 2, 3, 5, 6, 6, 7, 7, 8, 9];

    // constants
    const RANGE = { bottom: 6, top: 15 };
    const RANGE_UPDATE = 1;
    const NUM_NOTES_RANGE_UPDATE = 10;
    const STARTING_NOTE = 12;
    const NUM_NOTES = 8 * 48;

    const container = [];
    let up_p = 0.5;
    let half_p = 0.5;
    let intervalic_p = 0.3;
    let rest_p = 0.0;
    let counter = 0;
    let go_up = true;

    let direction = Math.random() < up_p ? 1 : -1;
    let step_size = Math.random() < half_p ? MAIN_INTERVALS[0] : MAIN_INTERVALS[1];
    let current_pitch = STARTING_NOTE;

    const dom = new JSDOM('');
    global.document = dom.window.document;

    for (let i = 0; i < NUM_NOTES; i++) {
        current_pitch = current_pitch + step_size * direction;
        container.push(current_pitch);

        up_p = direction === 1 ? up_p - 0.4 : up_p + 0.4;
        if (step_size === MAIN_INTERVALS[0]) {
            half_p = half_p - 0.4;
        } else if (step_size === MAIN_INTERVALS[1]) {
            half_p = half_p + 0.4;
        }
        intervalic_p = intervalic_p + 0.15;
        rest_p = rest_p + 0.0;

        if (current_pitch <= RANGE.bottom) {
            up_p = 1;
        } else if (current_pitch >= RANGE.top) {
            up_p = 0;
        }
        direction = Math.random() < up_p ? 1 : -1;

        step_size = Math.random() < half_p ? MAIN_INTERVALS[0] : MAIN_INTERVALS[1];

        if (Math.random() < intervalic_p) {
            step_size = EXTRA_INTERVALS[Math.floor(Math.random() * EXTRA_INTERVALS.length)];
            intervalic_p = 0.3;
        }

        if (Math.random() < rest_p) {
            container.push("r8");
            rest_p = 0.0;
        }

        if (i % NUM_NOTES_RANGE_UPDATE === 0) {
            if (go_up) {
                RANGE.bottom = RANGE.bottom + RANGE_UPDATE;
                RANGE.top = RANGE.top + RANGE_UPDATE;
                counter = counter + 1;
            } else {
                RANGE.bottom = RANGE.bottom - RANGE_UPDATE;
                RANGE.top = RANGE.top - RANGE_UPDATE;
                counter = counter - 1;
            }
            if (counter % 10 === 0) {
                go_up = true;
            } else if (counter % 10 === 5) {
                go_up = false;
            }
        }
    }

    console.log(container)

    // Generate the SVG representation
    const svgContainer = document.createElement('div')
    const renderer = new Vex.Renderer(
        svgContainer, Vex.Renderer.Backends.SVG
    );
    renderer.resize(800, 400);
    const context = renderer.getContext();

    const stave = new Vex.Stave(10, 40, 750);
        // Add a clef and time signature.
stave.addClef('treble').addTimeSignature('4/4');
    // const notes = container.map(pitch => {
    //     if (typeof pitch === "number") {
    //         return new Vex.StaveNote({
    //             keys: [pitch.toString()],
    //             duration: "8"
    //         });
    //     } else {
    //         return new Vex.StaveNote({
    //             keys: ["b/4"],
    //             duration: "8"
    //         }).addModifier(0, new Vex.Annotation(pitch));
    //     }
    // });

    const voice = new Vex.Voice({ num_beats: 4, beat_value: 4 });


    // Connect it to the rendering context and draw!
    stave.setContext(context).draw();
    // voice.addTickables(notes);

    const svgContent = svgContainer.querySelector('svg').outerHTML;
    // append this inside the svg tag: 
    // xmlns="http://www.w3.org/2000/svg"

    // Save the SVG to a file
    // const svgContent = renderer.svg();
    fs.writeFileSync(path.join(__dirname, 'output.svg'), svgContent, 'utf-8');
};

main();