<?php
function getGpsData($conexion, $IdUsuario, $data)  {
    $fechaInicio = isset($data->inicio) ? $data->inicio : "None";
    $fechaFin = isset($data->fin) ? $data->fin : "None";
    $id_parcela = $data->id_parcela;
    // $numeros_vaca = isset($data->numerosVacas) ? implode(',', $data->numerosVacas) : ""; // Convierte array a string separado por comas, maneja el caso donde $data->numerosVacas podría no estar definido

    if (isset($data->numerosVacas) && is_array($data->numerosVacas)) {
        // Limpia cada elemento del array
        $numerosVaca = array_map('trim', $data->numerosVacas);
        // Convierte el array a una cadena, separando los elementos con comas
        $numeros_vaca = implode(',', $numerosVaca);
    } else {
        $numeros_vaca = "";
    }

    if (isset($IdUsuario)) {
        // $comando = escapeshellcmd("python python/conjunto_de_datos_rapido.py '$IdUsuario' '$fechaInicio' '$fechaFin' '$numeros_vaca'");
        // Construye el comando asegurando que no haya saltos de línea ni caracteres adicionales
        $comando = escapeshellcmd("python python/conjunto_de_datos_rapido.py '$IdUsuario' '$id_parcela' '$fechaInicio' '$fechaFin' '$numeros_vaca'");
        $comando = str_replace(PHP_EOL, '', $comando); // Elimina saltos de línea del comando
        exec($comando, $salida,$codigo_retorno);
        if ($codigo_retorno == 0) {
            // La salida de exec está en un array, cada elemento es una línea de la salida
            $json_output = implode("\n", $salida);  // Convierte la salida en una sola cadena
            echo $json_output;  // Muestra o procesa el JSON
        } else {
            echo json_encode(["mensaje" => "Error al ejecutar el script de Python. Código de retorno: $codigo_retorno"]);
        }

    } else {
        echo json_encode(["mensaje" => "ID de usuario no especificado"]);
    }
}
