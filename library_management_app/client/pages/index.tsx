import type { NextPage } from "next";
import Library from "../utils/Library.json";
import { ethers } from "ethers";
import { LibraryContractAddress } from "../config";
import { useEffect, useState } from "react";
const Home: NextPage = () => {
  const [currentAccount, setCurrentAccount] = useState();
  const [books, setBooks] = useState();

  const connectToWallet = async () => {
    console.log("Connect To Wallet!");
    const { ethereum } = window;
    if (!ethereum) {
      window.alert("No Metamask detected!");
      return;
    }

    console.log(ethereum);

    const chainId = await ethereum.request({ method: "eth_chainId" });

    console.log("Chain Id : ", chainId);

    if (chainId !== "0x5") {
      console.log("Change wallet request...");
      await ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: "0x5" }],
      });
    }

    const accounts = await ethereum.request({
      method: "eth_requestAccounts",
    });

    console.log("Accounts : ", accounts[0]);

    setCurrentAccount(accounts[0]);
  };

  useEffect(() => {
    const { ethereum } = window;
    if (ethereum) {
      connectToWallet();

      // Create a new Web3Provider instance
      const web3Provider = new ethers.BrowserProvider(ethereum);

      // Create a new Signer instance using the current account
      web3Provider.getSigner().then((signer) => {
        console.log("Signer", signer);

        const LibraryContract = new ethers.Contract(
          LibraryContractAddress,
          Library.abi,
          signer
        );

        LibraryContract.getFinishedBooks().then((response) => {
          console.log(response);
        });
      });
    }
  }, []);

  return (
    <div className="space-y-2">
      <div className="text-center p-4">
        Hello From Web3 | Smart Contract | Solidity | Ethereum | React
      </div>
      <hr />
      <div className="flex flex-col p-2 align-middle justify-center">
        {currentAccount ? (
          <p>Connected With {currentAccount}</p>
        ) : (
          <div className="flex flex-col align-middle">
            <button
              onClick={connectToWallet}
              className="pl-4 pr-4 pt-2 pb-2 bg-blue-500 text-white"
            >
              Connect To Wallet
            </button>

            <div>
              <p>Books List</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
