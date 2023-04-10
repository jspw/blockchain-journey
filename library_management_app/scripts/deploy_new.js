const { ethers } = require("hardhat");

const main = async () => {
  const contractFactory = await ethers.getContractFactory("Library");
  const contract = await contractFactory.deploy();
  await contract.deployed();
  console.log("Contract Deployed to : ", contract.address);
  // Contract Deployed to :  0x770D5c9ba91b8A1b4EF293BB09D587dB758C3a83s
};

const runMain = async () => {
  try {
    await main();
    process.exit(0);
  } catch (error) {
    console.log(error);
    process.exit(1);
  }
};

runMain();
