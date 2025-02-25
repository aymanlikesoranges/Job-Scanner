(function() {
    if (window.location.href.includes("job")) {
        function safeFill(input, value) {
            if (input) {
                input.value = value;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }

        function safeSelect(selector, value) {
            let dropdown = document.querySelector(selector);
            if (dropdown) {
                let event = new Event('change', { bubbles: true });
                dropdown.value = value;
                dropdown.dispatchEvent(event);
            } else {
                console.warn(`${selector} dropdown not found.`);
            }
        }

        function fillFields() {
            let filled = false;

            const fields = [
                { selector: "input[id*='first'], input[name*='first'], input[aria-label*='first']", value: "Ayman" },
                { selector: "input[id*='last'], input[name*='last'], input[aria-label*='last']", value: "Uddin" },
                { selector: "input[id*='email'], input[name*='email'], input[aria-label*='email']", value: "auddin6@binghamton.edu" },
                { selector: "input[id*='phone'], input[name*='phone'], input[aria-label*='phone']", value: "9292153391" },
                { selector: "textarea[id*='cover'], textarea[name*='cover'], textarea[aria-label*='cover']", value: "I am very interested in this role and believe my skills match the job description." },
                { selector: "input[id*='linkedin'], input[name*='linkedin'], input[aria-label*='linkedin']", value: "https://www.linkedin.com/in/ayman-uddin/" }
            ];

            const dropdowns = [
                { selector: "div.select__input-container input[id*='school'], div.select__input-container input[name*='school']", value: "Binghamton University - SUNY" },
                { selector: "div.select__input-container input[id*='degree'], div.select__input-container input[name*='degree']", value: "Bachelor's degree" },
                { selector: "div.select__input-container input[id*='discipline'], div.select__input-container input[name*='discipline']", value: "Computer Science"},
                { selector: "select[id*='start-month'], select[name*='start-month']", value: "August" },
                { selector: "select[id*='start-year'], select[name*='start-year']", value: "2023" },
                { selector: "select[id*='end-month'], select[name*='end-month']", value: "May" },
                { selector: "select[id*='end-year'], select[name*='end-year']", value: "2027" },
                { selector: "select[id*='gender'], select[name*='gender'], select[aria-label*='gender']", value: "Male" },
                { selector: "select[id*='hispanic'], select[name*='hispanic'], select[aria-label*='hispanic']", value: "No" }
            ];

            fields.forEach(field => {
                let input = document.querySelector(field.selector);
                if (input) {
                    safeFill(input, field.value);
                    filled = true;
                } else {
                    console.warn(`${field.selector} field not found.`);
                }
            });

            dropdowns.forEach(dropdown => {
                safeSelect(dropdown.selector, dropdown.value);
            });

            if (!filled) {
                console.log("No matching fields were found to autofill.");
            }
        }

        setTimeout(function() {
            fillFields();

            let form = document.querySelector("form");
            if (form) {
                form.addEventListener("submit", function(event) {
                    event.preventDefault();
                    form.submit();
                });
            }
        }, 5000);
    }
})();