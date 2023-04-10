const { expect } = require("chai");
const { ethers } = require("hardhat");

const getRandomInt = (min, max) => {
  return Math.floor(Math.random() * (max - min)) + min;
};

function verifyBook(bookChain, book) {
  expect(book.name).to.equal(bookChain.name);
  expect(book.year.toString()).to.equal(bookChain.year.toString());
  expect(book.author).to.equal(bookChain.author);
}

function verifyBookList(booksFromChain, bookList) {
  expect(booksFromChain.length).to.not.equal(0);
  expect(booksFromChain.length).to.equal(bookList.length);
  for (let i = 0; i < bookList.length; i++) {
    const bookChain = booksFromChain[i];
    const book = bookList[i];
    verifyBook(bookChain, book);
  }
}

describe("Library Contract", function () {
  let Library;
  let library;
  let owner;

  const NUM_UNFINISHED_BOOKS = 5;
  const NUM_FINISHED_BOOKS = 3;

  let unfinishedBookList;
  let finishedBookList;

  beforeEach(async function () {
    Library = await ethers.getContractFactory("Library");
    [owner] = await ethers.getSigners();
    library = await Library.deploy();

    unfinishedBookList = [];
    finishedBookList = [];

    for (let i = 0; i < NUM_FINISHED_BOOKS; i++) {
      let book = {
        name: getRandomInt(0, 100).toString(),
        year: getRandomInt(2000, 2022),
        author: getRandomInt(0, 100).toString(),
        isFinished: true,
      };
      await library.addBook(book.name, book.year, book.author, book.isFinished);
      finishedBookList.push(book);
    }

    for (let i = 0; i < NUM_UNFINISHED_BOOKS; i++) {
      let book = {
        name: getRandomInt(0, 100).toString(),
        year: getRandomInt(2000, 2022),
        author: getRandomInt(0, 100).toString(),
        isFinished: false,
      };
      await library.addBook(book.name, book.year, book.author, book.isFinished);
      unfinishedBookList.push(book);
    }
  });

  describe("Add Book", function () {
    it("Should emit AddBook event", async function () {
      let book = {
        name: getRandomInt(0, 100).toString(),
        year: getRandomInt(2000, 2022),
        author: getRandomInt(0, 100).toString(),
        isFinished: false,
      };

      await expect(
        await library.addBook(
          book.name,
          book.year,
          book.author,
          book.isFinished
        )
      )
        .emit(library, "AddBook")
        .withArgs(owner.address, NUM_FINISHED_BOOKS + NUM_UNFINISHED_BOOKS);
    });
  });

  describe("Get Books", function () {
    it("Should return the list of the unfinished books", async function () {
      const booksFromChain = await library.getUnfinishedBooks();
      expect(booksFromChain.length).to.equal(NUM_UNFINISHED_BOOKS);
      verifyBookList(booksFromChain, unfinishedBookList);
    });

    it("Should return the list of the finished books", async function () {
      const booksFromChain = await library.getFinishedBooks();
      expect(booksFromChain.length).to.equal(NUM_FINISHED_BOOKS);
      verifyBookList(booksFromChain, finishedBookList);
    });
  });

  describe("Set Finished", function () {
    it("Should emit SetFinished event", async function () {
      const BOOK_ID = 0;

      await expect(library.setBookFinished(BOOK_ID))
        .to.emit(library, "SetBookFinished")
        .withArgs(BOOK_ID);
    });
  });
});
