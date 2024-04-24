<?php
include 'conexion.php';
include 'funciones/helpers.php';  // Se asume la existencia de un archivo con funciones auxiliares

include 'funciones/vacas.php'; 
include 'funciones/parcelas.php'; 

session_start();
header("Content-Type: application/json");
ensureRequestMethod($_SERVER['REQUEST_METHOD']);

$uri = getRequestUri($_SERVER['REQUEST_URI']);

// Verificar sesión de usuario
$IdUsuario = getSessionUserId();  // Esta función debe manejar la lógica de obtener el ID del usuario o fallar si no está logueado

switch ($_SERVER['REQUEST_METHOD']) {
    case 'GET':
        handleGetRequest($uri, $conexion, $IdUsuario);
        break;

    case 'POST':
        $data = json_decode(file_get_contents('php://input'), true);
        handlePostRequest($uri, $conexion, $IdUsuario, $data);
        break;

    case 'PUT':
        $data = json_decode(file_get_contents('php://input'), true);
        handlePutRequest($uri, $conexion, $IdUsuario, $data);
        break;

    case 'DELETE':
        handleDeleteRequest($uri, $conexion, $IdUsuario);
        break;

    default:
        responseError(404, 'Not Found');
        break;
}

function handleGetRequest($uri, $conexion, $IdUsuario) {
    switch ($uri[1]) {
        case 'parcelas':
            getParcelas($conexion, $IdUsuario);
            break;
        case 'vacas':
            getVacasDetails($uri, $conexion, $IdUsuario);
            break;
        default:
            responseError(404, 'Not Found');
    }
}

function handlePostRequest($uri, $conexion, $IdUsuario, $data) {
    switch ($uri[1]) {
        case 'gps':
            getGpsData($conexion, $IdUsuario, $data);
            break;
        case 'sectores':
            if ($uri[2] = 'recomendar'){
                recomendarSector( $conexion, $IdUsuario, $data);
            }else{
                addSector( $conexion, $IdUsuario, $data);
            }
            break;
        default:
            responseError(404, 'Not Found');
    }
}

function handlePutRequest($uri, $conexion, $IdUsuario, $data) {
    switch ($uri[1]) {
        case 'sectores':
            // Actualizar el sector
            updateSectores($conexion, $IdUsuario, $data); 
            break;
        default:
            responseError(404, 'Not Found');
    }
}

function handleDeleteRequest($uri, $conexion, $IdUsuario) {
    switch ($uri[1]) {
        case 'sectores':
            // Eliminar el sector
            deleteSector($conexion, $uri[2]); 
            break;
        default:
            responseError(404, 'Not Found');
    }
}

