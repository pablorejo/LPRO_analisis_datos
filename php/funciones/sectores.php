
<?php
function addSector($conexion, $IdUsuario, $data) {

    $id_parcela = $data->id_parcela;
    // Insertar la información de la parcela en la tabla 'parcela'
    $sentencia = $conexion->prepare("INSERT INTO sector (id_parcela, IdUsuario) VALUES (?, ?)");
    $sentencia->bind_param("ii", $id_parcela, $IdUsuario);
    $sentencia->execute();
    
    // Obtener el id_parcela recién insertado
    $id_sector = $sentencia->insert_id;
    
    // Insertar las coordenadas en la tabla 'coordenadas'
    $coordenadas = $data->coordenadasSector;
    
    foreach ($coordenadas as $coordenada) {
        $latitud = $coordenada->latitude;
        $longitud = $coordenada->longitude;
        
        $sentenciaCoordenadas = $conexion->prepare("INSERT INTO coordenadas_sector (id_sector, id_parcela, latitude, longitude) VALUES (?,?,?,?)");
        $sentenciaCoordenadas->bind_param("iidd", $id_sector,$id_parcela , $latitud, $longitud);
        $sentenciaCoordenadas->execute();
    }
    
    // Verificar si la inserción fue exitosa
    if ($sentencia->affected_rows > 0) {
        echo json_encode(["mensaje" => "Parcela y coordenadas insertadas correctamente"]);
    } else {
        echo json_encode(["mensaje" => "Error al insertar parcela y coordenadas"]);
    }
}

function updateSectores($conexion, $IdUsuario, $data) {
    // Obtener los datos de la parcela
    $id_parcela = $data->id_parcela;
    $id_sector = $data->id_sector;

    $actualizoAlgunaCoordenada = false;
    $coordenadas = $data->coordenadasSector;

    $sqlDelete = $conexion->prepare("DELETE FROM coordenadas_sector WHERE id_parcela = ? AND id_sector = ?");
    $sqlDelete->bind_param("ii", $id_parcela , $id_sector);
    $sqlDelete->execute();

    foreach ($coordenadas as $coordenada) {
        $latitud = $coordenada->latitude;
        $longitud = $coordenada->longitude;
        
        $sentenciaCoordenadas = $conexion->prepare("INSERT INTO coordenadas_sector (id_sector, id_parcela, latitude, longitude) VALUES (?,?,?,?)");
        $sentenciaCoordenadas->bind_param("iidd", $id_sector,$id_parcela , $latitud, $longitud);
        $sentenciaCoordenadas->execute();
    }
    echo json_encode(["mensaje" => "sector actualizado correctamente"]);
}
function deleteSector($conexion, $id_sector) {

    // Iniciar una transacción para garantizar la consistencia de los datos
    $conexion->begin_transaction();

    // Eliminar las coordenadas asociadas a la parcela, esto igual no hace falta ya que en parcela tenemos on delete cascade
    $sentenciaEliminarCoordenadas = $conexion->prepare("DELETE FROM coordenadas_sector WHERE id_sector = ?");
    $sentenciaEliminarCoordenadas->bind_param("i", $id_sector);
    $sentenciaEliminarCoordenadas->execute();

    // Eliminar la parcela
    $sentenciaEliminarParcela = $conexion->prepare("DELETE FROM sector WHERE id_sector = ?");
    $sentenciaEliminarParcela->bind_param("i", $id_sector);
    $sentenciaEliminarParcela->execute();

    // Verificar si la parcela y las coordenadas asociadas fueron eliminadas correctamente
    if ($sentenciaEliminarParcela->affected_rows > 0) {
        // Confirmar la transacción si todo fue exitoso
        $conexion->commit();
        echo json_encode(["mensaje" => "Parcela y coordenadas eliminadas correctamente"]);
    } else {
        // Revertir la transacción si hubo un error
        $conexion->rollback();
        echo json_encode(["mensaje" => "Error al eliminar parcela y coordenadas"]);
    }
}

function recomendarSector($conexion, $IdUsuario, $data){
    $id_parcela = $data->id_parcela;
    // $comando = escapeshellcmd("python python/conjunto_de_datos_rapido.py '$IdUsuario' '$fechaInicio' '$fechaFin' '$numeros_vaca'");
    // Construye el comando asegurando que no haya saltos de línea ni caracteres adicionales
    $comando = escapeshellcmd("python3 python/recomendar_sector.py '$IdUsuario' '$id_parcela'");
    $comando = str_replace(PHP_EOL, '', $comando); // Elimina saltos de línea del comando

    exec($comando, $salida,$codigo_retorno);
    if ($codigo_retorno == 0) {
        // La salida de exec está en un array, cada elemento es una línea de la salida
        $json_output = implode("\n", $salida);  // Convierte la salida en una sola cadena
        echo $json_output;  // Muestra o procesa el JSON
    } else if ($codigo_retorno == 128){
        echo json_encode(["mensaje" => "No existe es sector de la parcela '$id_parcela'"]);
    }else if ($codigo_retorno == 129){
        echo json_encode(["mensaje" => "Ha entrado en un bucle infinito"]);
    }else {
        echo json_encode(["mensaje" =>  "Error al ejecutar el script de Python. Código de retorno: $codigo_retorno"]);
    }
}

