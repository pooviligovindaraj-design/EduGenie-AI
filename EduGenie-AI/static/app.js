const state = {
    task: "qa"
};


const labels = {

    qa: {

        title: "Ask your question",

        placeholder:
            "Example: Why does the sky look blue?"

    },


    explain: {

        title:
            "What should EduGenie explain?",

        placeholder:
            "Example: Explain the Pythagorean theorem with a simple analogy."

    },


    quiz: {

        title:
            "Paste a passage or study material",

        placeholder:
            "Paste at least a few paragraphs of notes, textbook content, or a topic passage here."

    },


    summarize: {

        title:
            "Paste the text to summarize",

        placeholder:
            "Paste a long educational passage here."

    },


    learn: {

        title:
            "What do you want to learn?",

        placeholder:
            "Example: SQL from beginner to job-ready"

    }

};


const taskButtons =
    document.querySelectorAll(
        ".task-tab"
    );


const inputLabel =
    document.querySelector(
        "#input-label"
    );


const input =
    document.querySelector(
        "#user-input"
    );


const lengthWrap =
    document.querySelector(
        "#length-wrap"
    );


const hoursWrap =
    document.querySelector(
        "#hours-wrap"
    );


const form =
    document.querySelector(
        "#task-form"
    );


const button =
    document.querySelector(
        "#submit-button"
    );


const resultSection =
    document.querySelector(
        "#result-section"
    );


const result =
    document.querySelector(
        "#result"
    );


const resultTitle =
    document.querySelector(
        "#result-title"
    );


const copyButton =
    document.querySelector(
        "#copy-button"
    );



/* -------------------------------------------------------
   TASK SELECTION
------------------------------------------------------- */

function setTask(task) {

    state.task = task;


    taskButtons.forEach(
        btn => {

            btn.classList.toggle(
                "active",
                btn.dataset.task === task
            );

        }
    );


    inputLabel.textContent =
        labels[task].title;


    input.placeholder =
        labels[task].placeholder;


    lengthWrap.classList.toggle(
        "hidden",
        task !== "summarize"
    );


    hoursWrap.classList.toggle(
        "hidden",
        task !== "learn"
    );

}


taskButtons.forEach(
    btn => {

        btn.addEventListener(
            "click",
            () => {

                setTask(
                    btn.dataset.task
                );

            }
        );

    }
);



/* -------------------------------------------------------
   HEALTH CHECK
------------------------------------------------------- */

async function checkHealth() {

    const dot =
        document.querySelector(
            "#status-dot"
        );


    const text =
        document.querySelector(
            "#status-text"
        );


    try {

        const response =
            await fetch(
                "/health"
            );


        const data =
            await response.json();


        if (
            data.status === "ok"
            &&
            data.gemini_configured
        ) {

            dot.style.background =
                "var(--success)";

            text.textContent =
                "Backend + Gemini ready";

        } else {

            text.textContent =
                "Backend ready · API key missing";

        }


    } catch {

        text.textContent =
            "Backend unavailable";

        dot.style.background =
            "var(--danger)";

    }

}



/* -------------------------------------------------------
   QUIZ RENDERING
------------------------------------------------------- */

function renderQuiz(
    questions
) {

    result.innerHTML = "";


    questions.forEach(
        (q, index) => {

            const card =
                document.createElement(
                    "article"
                );


            card.className =
                "quiz-question";


            const title =
                document.createElement(
                    "h3"
                );


            title.textContent =
                `${index + 1}. ${q.question}`;


            card.appendChild(
                title
            );


            q.options.forEach(
                option => {

                    const optionButton =
                        document.createElement(
                            "button"
                        );


                    optionButton.className =
                        "option";


                    optionButton.textContent =
                        option;


                    optionButton.type =
                        "button";


                    optionButton.addEventListener(
                        "click",
                        () => {

                            card
                                .querySelectorAll(
                                    ".option"
                                )
                                .forEach(
                                    b => {
                                        b.disabled = true;
                                    }
                                );


                            if (
                                option ===
                                q.correct_answer
                            ) {

                                optionButton
                                    .classList
                                    .add(
                                        "correct"
                                    );


                                feedback.textContent =
                                    "✓ Correct!";

                            } else {

                                optionButton
                                    .classList
                                    .add(
                                        "wrong"
                                    );


                                card
                                    .querySelectorAll(
                                        ".option"
                                    )
                                    .forEach(
                                        b => {

                                            if (
                                                b.textContent
                                                ===
                                                q.correct_answer
                                            ) {

                                                b.classList
                                                    .add(
                                                        "correct"
                                                    );

                                            }

                                        }
                                    );


                                feedback.textContent =
                                    `✗ Not quite. Correct answer: ${q.correct_answer}`;

                            }


                            explanation.textContent =
                                q.explanation || "";

                        }
                    );


                    card.appendChild(
                        optionButton
                    );

                }
            );


            const feedback =
                document.createElement(
                    "div"
                );


            feedback.className =
                "feedback";


            card.appendChild(
                feedback
            );


            const explanation =
                document.createElement(
                    "div"
                );


            explanation.className =
                "feedback";


            card.appendChild(
                explanation
            );


            result.appendChild(
                card
            );

        }
    );

}



/* -------------------------------------------------------
   FORM SUBMISSION
------------------------------------------------------- */

form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        const text =
            input.value.trim();


        if (!text) {
            return;
        }


        button.disabled = true;

        button.textContent =
            "Thinking…";


        resultSection.classList.remove(
            "hidden"
        );


        resultTitle.textContent =
            "EduGenie is working…";


        result.textContent =
            "";


        const level =
            document.querySelector(
                "#level"
            ).value;


        let endpoint;

        let body = {
            level: level
        };


        /* Q&A */

        if (
            state.task === "qa"
        ) {

            endpoint = "/qa";

            body.question = text;

        }


        /* Explanation */

        else if (
            state.task === "explain"
        ) {

            endpoint = "/explain";

            body.topic = text;

            body.style = "simple";

        }


        /* Quiz */

        else if (
            state.task === "quiz"
        ) {

            endpoint = "/quiz";

            body.text = text;

        }


        /* Summary */

        else if (
            state.task === "summarize"
        ) {

            endpoint =
                "/summarize";

            body.text = text;

            body.length =
                document.querySelector(
                    "#summary-length"
                ).value;

        }


        /* Learning path */

        else {

            endpoint =
                "/learn/recommendations";

            body.topic = text;

            body.hours_per_week =
                Number(
                    document.querySelector(
                        "#hours"
                    ).value
                );

        }


        try {

            const response =
                await fetch(
                    endpoint,
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(body)

                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Request failed."
                );

            }


            resultTitle.textContent =
                state.task === "quiz"
                    ? "Your 3-question quiz"
                    : "EduGenie result";


            if (
                state.task === "quiz"
            ) {

                renderQuiz(
                    data.questions
                );

            } else {

                result.textContent =
                    data.result;

            }


        } catch (error) {

            resultTitle.textContent =
                "Something went wrong";


            result.textContent =
                error.message;


        } finally {

            button.disabled =
                false;


            button.textContent =
                "Run EduGenie";

        }

    }
);



/* -------------------------------------------------------
   COPY
------------------------------------------------------- */

copyButton.addEventListener(
    "click",
    async () => {

        try {

            await navigator.clipboard.writeText(
                result.innerText
            );


            copyButton.textContent =
                "Copied!";


            setTimeout(
                () => {

                    copyButton.textContent =
                        "Copy";

                },
                1200
            );


        } catch {

            copyButton.textContent =
                "Copy failed";

        }

    }
);



/* -------------------------------------------------------
   INITIALIZE
------------------------------------------------------- */

setTask("qa");

checkHealth();