document.addEventListener("DOMContentLoaded", function() {
    // Initialize CodeMirror for the code editor
    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        lineNumbers: true,
        mode: "python",
        indentUnit: 4,
        indentWithTabs: true,
        extraKeys: {
            "Ctrl-Space": function(cm) {
                cm.showHint({hint: CodeMirror.hint.anyword});
            }
        }
    });

    // Function to load the method's code into the editor
    window.loadMethod = function() {
        const methodName = "example_method"; // Adjust accordingly
        fetch(`/get_method/${methodName}`)
            .then(response => response.json())
            .then(data => editor.setValue(data.code))
            .catch(error => console.error('Error loading method:', error));
    };

    // Function to save the edited method's code
    window.saveMethod = function() {
        const methodName = "example_method"; // Adjust accordingly
        const code = editor.getValue();
        fetch(`/save_method/${methodName}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({code: code}),
        })
        .then(response => response.json())
        .then(data => alert(data.message))
        .catch(error => console.error('Error saving method:', error));
    };

    // Function to execute the code with the provided dictionary
    window.executeCode = function() {
        const code = editor.getValue();
        const inputDict = document.getElementById("input-dict").value;
        try {
            const parsedDict = JSON.parse(inputDict); // Parse the dictionary input
            fetch('/execute_code', { // Use the correct endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({code: code, input_dict: parsedDict}),
            })
            .then(response => response.json())
            .then(data => {
                if(data.error) {
                    document.getElementById("output").innerText = "Error: " + data.error;
                } else {
                    document.getElementById("output").innerText = "Result: " + data.result;
                }
            })
            .catch(error => console.error('Error executing code:', error));
        } catch (error) {
            console.error("Error parsing input dict:", error);
            document.getElementById("output").innerText = "Error in input dict format.";
        }
    };

        // Function to load method names into the selector
    function loadMethodNames() {
        fetch('/get_method_names')
            .then(response => response.json())
            .then(methodNames => {
                const select = document.getElementById("method-select");
                methodNames.forEach(name => {
                    const option = document.createElement("option");
                    option.value = name;
                    option.textContent = name;
                    select.appendChild(option);
                });
            })
            .catch(error => console.error('Error loading method names:', error));
    }

    loadMethodNames(); // Call this function to populate the selector on page load
});
