<?php

/**
 * Ensure the request method is supported; otherwise, send a 405 Method Not Allowed response.
 * 
 * @param string $method The request method from the server.
 */
function ensureRequestMethod($method) {
    $allowedMethods = ['GET', 'POST', 'PUT', 'DELETE'];
    if (!in_array($method, $allowedMethods)) {
        responseError(405, 'Method Not Allowed');
    }
}

/**
 * Parses and returns a clean URI array.
 * 
 * @param string $rawUri The raw URI obtained from $_SERVER['REQUEST_URI']
 * @return array The cleaned URI segments.
 */
function getRequestUri($rawUri) {
    $uri = parse_url($rawUri, PHP_URL_PATH);
    $uri = explode('/', trim($uri, '/'));
    return $uri;
}

/**
 * Fetches the user ID from the session or terminates if not found.
 * 
 * @return int The user ID from the session.
 */
function getSessionUserId() {
    if (!isset($_SESSION['user_id'])) {
        responseError(401, 'Unauthorized: No session present.');
    }
    return $_SESSION['user_id'];
}

/**
 * Send a JSON response with a status code and a message.
 * 
 * @param int $code The HTTP status code to send.
 * @param string $message The message to include in the response.
 */
function responseError($code, $message) {
    http_response_code($code);
    echo json_encode(['error' => $message]);
    exit;
}