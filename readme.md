## Solicitud para Evaluación y Presupuestación de un Sistema de Gestión Financiera  (Banco)
A través de la misma se solicita la evaluación y presupuestación de una plataforma online 
que permita el registro de clientes, validación de identidad, y apertura de caja de ahorro.
A través de la plataforma, los clientes deberán poder registrarse y dar de alta una cuenta 
bancaria. 

A aquellos clientes que soliciten la apertura de cuenta, se les otorgará un saldo inicial de 
$100000.
Se requiere que los clientes tengan la capacidad de:
- Registrarse como nuevos clientes
- Poseer una caja de ahorro, de alta automática durante el registro, con un saldo inicial de 
$100000.
- Generar códigos de autorización de débitos para utilizar en plataformas externas.
- Consultar el saldo y los movimientos de la cuenta.
La plataforma deberá tener la capacidad de recibir solicitudes de débitos desde distintos 
sistemas de terceros, utilizando un código de autorización, previamente generado.
Ante la solicitud de un débito, el sistema deberá recibir y validar un "token" generado 
previamente por el cliente, indicando un número de operación.
El token será utilizado por la entidad de 3ro, y deberá enviarlo de manera conjunta con un 
Nro de operación de referencia

## HOW TO USE

#### Create a python virtual env:
python -m venv myenv
pip install -r requirements.txt