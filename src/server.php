<?php
$data = json_decode(file_get_contents('php://input'), true);

if ($data && isset($data['servo_position'])) {
    $servo_position = $data['servo_position'];


    $response = array('status' => 'Success', 'message' => 'Servo position updated');
    header('Content-Type: application/json');
    echo json_encode($response);
} else {
    header('HTTP/1.1 400 Bad Request');
    echo 'Invalid or missing data';
}
