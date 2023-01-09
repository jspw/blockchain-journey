// SPDX-License-Identifier: MIT

pragma solidity ^0.8.8; // ^0.8.12 means above 0.8.12 is okey with this code | can be also >=0.8.7 < 0.9.0

contract SimpleStorage {
    int256 age = 12;
    string name = "Shifat";
    address myAddress = 0x75a9E717826593F405b7739eb26d79415E755089; // address of account
    bytes32 myBytes = "shft"; // will be converted into bytes automatically.

    uint256 num; //. this will initialized with 0

    function store(uint256 _num) public {
        num = _num;
    }

    // view | pure -> functions just read and dont use any gas, that's why it will be bluish color in the deplyed contract
    // it disallow modification of state
    // calling this function is free unless you call it inside code.

    function retrieve() public view returns (uint256) {
        return num;
    }

    function doAlgo() public pure returns (uint256) {
        return (1 + 5);
    }

    struct People {
        uint256 age;
        string name;
    }

    People public person = People({age: 20, name: "MH"});

    People[] public people; // People[5] means array size 5

    mapping(string => uint256) public nameToAge;

    // EVM can access and store information in six places
    // calldata is temporary data that can not be modified
    // memory is temporary data that can be
    // storage is permanent that can be modified. actually all other variables are stored in storage by default

    function addPerson(string memory _name, uint256 _age) public {
        people.push(People({name: _name, age: _age}));
        nameToAge[_name] = _age;
    }
}

// 0xd9145CCE52D386f254917e481eB44e9943F39138
