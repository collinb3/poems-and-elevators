#!/usr/bin/env node
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const BASE_ENDPOINT = "https://poetrydb.org";
function parseArgs() {
    const args = process.argv.slice(2);
    const parsed = {};
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === "--help" || arg === "-h") {
            parsed.help = true;
        }
        else if (arg === "--author" || arg === "-a") {
            parsed.author = args[++i];
        }
        else if (arg === "--title" || arg === "-t") {
            parsed.title = args[++i];
        }
        else if (arg === "--params" || arg === "-p") {
            parsed.params = args[++i];
        }
    }
    return parsed;
}
function showHelp() {
    console.log(`
Usage: node script.js [options]

Options (Should always be wrapped in quotes if they contain spaces):
  -a, --author "author name"                    Author name to fetch poems for
  -t, --title "poem title"                      Poem title to filter results
  -p, --params "author,title"                   (Optional) additional parameters (comma-separated)
                                                    - Accepted values: author, title, lines, linecount
  -h, --help                                    Show this help message

Examples:
  node script.js -a "Emily Dickinson"
  node script.js -a "Emily Dickinson" -p "author,title,linecount"

  node script.js --title  "Youth And Age"
  `);
}
async function makeApiCall(args) {
    try {
        let endpoint = BASE_ENDPOINT;
        const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "User-Agent": "CLI-Script/1.0",
            },
        };
        if (args.author && args.title) {
            const encodedAuthor = encodeURIComponent(args.author);
            const encodedTitle = encodeURIComponent(args.title);
            endpoint += `/author,title/${encodedAuthor};${encodedTitle}`;
        }
        else if (args.author) {
            const encodedAuthor = encodeURIComponent(args.author);
            endpoint += `/author/${encodedAuthor}`;
        }
        else if (args.title) {
            const encodedTitle = encodeURIComponent(args.title);
            endpoint += `/title/${encodedTitle}`;
        }
        if (args.params) {
            // Clean up params - remove spaces around commas
            const cleanParams = args.params.replace(/\s*,\s*/g, ",").trim();
            const encodedParams = encodeURIComponent(cleanParams);
            endpoint += `/${encodedParams}`;
        }
        console.log("Making request to:", endpoint);
        const response = await fetch(endpoint, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status} ${response.statusText}`);
        }
        const data = await response.json();
        if (data.status && data.status === 404) {
            console.error("Error: No record found. Please check your spelling or try another author/title.");
            process.exit(1);
        }
        console.log("\nResponse Data:");
        console.log(JSON.stringify(data, null, 2));
    }
    catch (error) {
        console.error("Error making API call:");
        if (error instanceof Error) {
            console.error("Message:", error.message);
        }
        else {
            console.error("Unknown error:", error);
        }
        process.exit(1);
    }
}
async function main() {
    const args = parseArgs();
    if (args.help) {
        showHelp();
        return;
    }
    if ((!args.author && !args.title)) {
        console.error("Error: No author or title argument provided. Use --help for usage information.");
        process.exit(1);
    }
    await makeApiCall(args);
}
// Handle unhandled promise rejections
process.on("unhandledRejection", (reason, promise) => {
    console.error("Unhandled Rejection at:", promise, "reason:", reason);
    process.exit(1);
});
// Handle uncaught exceptions
process.on("uncaughtException", (error) => {
    console.error("Uncaught Exception:", error);
    process.exit(1);
});
// Run the main function
main().catch((error) => {
    console.error("Script failed:", error);
    process.exit(1);
});
