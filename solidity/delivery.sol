pragma solidity ^0.8.18;

contract Delivery {
    address payable owner_address;
    address payable courier_address;
    address customer_address;
    uint delivery_price;
    bool paid;
    bool delivered;

    // Ideja - kurir moze da preuzme ugovor i ne moze i ne mora da ga dostavi pre nego sto ga kupac plati

    constructor(
        address payable _owner_address,
        address payable _courier_address,
        address _customer_address,
        uint _delivery_price
    ) {
        owner_address = _owner_address;
        courier_address = _courier_address;
        customer_address = _customer_address;
        delivery_price = _delivery_price;
    }

    function pay() external payable {
        // da nije vec placen
        require(msg.sender == customer_address, "Invalid customer address!");
        require(msg.value == delivery_price, "Insufficient funds!");
        require(paid == false, "Delivery already payed!");

        paid = true;
    }

    function confirm_delivery(int courier_type) external payable {
        // potvrda dostave
        require(msg.sender == customer_address, "Invalid customer address!");
        require(paid == true, "Delivery not paid!");
        require(delivered == false, "Delivery already confirmed!");

        delivered = true;

        // pola vlasniku servisa - ostatak kuriru
        uint owner_amount = 0;
        uint courier_amount = 0;

        if (courier_type == 0) {
            // 20 posto kuriru
            courier_amount = delivery_price / 5;
        } else if (courier_type == 1) {
            // 30 posto kuriru
            courier_amount = (delivery_price * 3) / 10;
        } else if (courier_type == 2) {
            // 50 posto kuriru
            courier_amount = delivery_price / 2;
        }

        owner_amount = delivery_price - courier_amount;

        // nakon promene - ugovor prevesti, pa customer kontejner promeniti
        owner_address.transfer(owner_amount);
        courier_address.transfer(courier_amount);
    }
}
