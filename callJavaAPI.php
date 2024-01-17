<?php
// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $arg1 = $_POST["arg1"];
    // Execute the Java command and capture the output and errors
    $command = 'java -cp ".:java_lib/*" java_src/Main.java ' . escapeshellarg($arg1);
    $output = shell_exec($command);
    
    if ($output !== null) {
        // Java program executed successfully
        http_response_code(200); // HTTP status code for success
        echo $output; // Send the output to the client
    } else {
        // Java program encountered an error
        http_response_code(500); // HTTP status code for internal server error
        echo "Error executing Java program.";
    }
} else {
    // Return a bad request response if not submitted via POST
    http_response_code(400); // HTTP status code for bad request
    echo "Bad request.";
}
?>