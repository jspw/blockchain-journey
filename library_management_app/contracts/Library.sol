//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;

contract Library {

    event AddBook(address recipient,uint bookId);
    event SetBookFinished(uint bookId);

    struct Book {
        uint256 id;
        string name;
        uint256 year;
        string author;
        bool isFinished;
    }

    Book[] private bookList;

    mapping(uint256 => address) bookToOwner;

    function addBook(
        string memory name,
        uint16 year,
        string memory author,
        bool isFinished
    ) external {
        uint256 bookId = bookList.length;
        bookList.push(Book(bookId,name,year,author,isFinished));
        bookToOwner[bookId] = msg.sender;
        emit AddBook(msg.sender, bookId);
    }

    function _getBookList(bool isFinished) private view returns (Book[] memory){
        Book[] memory temp = new Book[](bookList.length);
        uint count = 0;
        for(uint i=0;i<bookList.length;i++){
            if(bookToOwner[i] == msg.sender && bookList[i].isFinished == isFinished){
                temp[count] = bookList[i];
                count++;
            }
        }

        Book[] memory result = new Book[](count);
        for(uint i=0;i<count;i++){
            result[i] = temp[i];
        }

        return result;
    }

    function getFinishedBooks() external view returns (Book [] memory){
        return _getBookList(true);
    }

    function getUnfinishedBooks () external view returns (Book[] memory){
        return _getBookList(false);
    }

    function setBookFinished (uint bookId) external {
        if(bookToOwner[bookId] == msg.sender){
            bookList[bookId].isFinished = true;
            emit SetBookFinished(bookId);
        }
    }
}
