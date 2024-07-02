function randRange(min, max) {
    return Math.floor((max - min) * Math.random()) + min;
}

function randString(len) {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let str = "";
    for (let i = 0; i != len; i++) {
        str += chars.charAt(randRange(0, chars.length));
    }
    return str;
}

//
//

const svgNamespace = "http://www.w3.org/2000/svg";
const bookColors = [ "#8D544B", "#446463", "#AA483B", "#89969F", "#56565E", "#EFB561", "#749159", "#8E5053" ];
let bookshelfElem = undefined;
let bookshelfState = [ ];
let tableElem = undefined;
let tableState = { };
let bookLookup = { };

//
//

function bookGetInfo(book) {
    return bookLookup[book.getAttribute("id")];
}

function bookSetUpright(book, bookInfo) {
    book.setAttribute("width", bookInfo.width.toString());

    let paper = book.getElementById("paper");
    paper.style = { };
    paper.style.display = "none"

    let spine = book.getElementById("spine");
    spine.setAttribute("width", bookInfo.width.toString());
    spine.setAttribute("height", bookInfo.height.toString());
    spine.setAttribute("fill", bookInfo.color);

    let shadow = book.getElementById("shadow");
    shadow.setAttribute("width", (bookInfo.width / 2).toString());
    shadow.setAttribute("height", bookInfo.height.toString());
    shadow.setAttribute("fill", "black");
    shadow.setAttribute("opacity", "15%");
    shadow.setAttribute("x", (bookInfo.width / 2).toString());
    shadow.setAttribute("y", 0);
    bookInfo.state = "upright";
}

function bookSetClosed(book, bookInfo) {
    book.setAttribute("width", bookInfo.depth.toString());
    
    let paper = book.getElementById("paper");
    paper.style.display = "none";
    
    let spine = book.getElementById("spine");
    spine.setAttribute("width", bookInfo.depth.toString());
    spine.setAttribute("height", bookInfo.height.toString());
    spine.setAttribute("fill", bookInfo.color);
    
    let shadow = book.getElementById("shadow");
    shadow.setAttribute("width", (bookInfo.depth / 2).toString());
    shadow.setAttribute("height", bookInfo.height.toString());
    shadow.setAttribute("fill", "black");
    shadow.setAttribute("opacity", "15%");
    shadow.setAttribute("x", (bookInfo.depth / 2).toString());
    shadow.setAttribute("y", 0);
    
    bookInfo.state = "closed";
}

function bookSetOpen(book, bookInfo) {
    book.setAttribute("width", (bookInfo.depth * 2).toString());
    
    let paper = book.getElementById("paper");
    paper.style.display = "block";
    paper.setAttribute("width", "100%");
    paper.setAttribute("height", "100%");
    paper.setAttribute("transform-origin", "50% 50%");
    paper.setAttribute("transform", "scale(.9)");
    paper.setAttribute("fill", "#f5edd6");
    paper.style.filter = "drop-shadow(3px 5px 2px rgb(0 0 0 / 0.4))";
    
    let spine = book.getElementById("spine");
    spine.setAttribute("width", (bookInfo.depth * 2).toString());
    spine.setAttribute("height", bookInfo.height.toString());
    spine.setAttribute("fill", bookInfo.color);
    
    let shadow = book.getElementById("shadow");
    shadow.setAttribute("width", (bookInfo.depth).toString());
    shadow.setAttribute("height", bookInfo.height.toString());
    shadow.setAttribute("fill", "black");
    shadow.setAttribute("opacity", "15%");
    shadow.setAttribute("x", (bookInfo.depth).toString());
    shadow.setAttribute("y", 0);
    
    bookInfo.state = "open";
}

function bookSetState(book, state) {
    let bookInfo = bookGetInfo(book);
    switch(state) {
        case "upright": bookSetUpright(book, bookInfo); break;
        case "closed":  bookSetClosed(book, bookInfo);  break;
        case "open":    bookSetOpen(book, bookInfo);    break;
    }
}   

function bookShow(book) {
    book.setAttribute("opacity", "100%");
}

function bookHide(book) {
    book.setAttribute("opacity", "0%");
}

function bookHighlight(book) {
    book.getElementById("spine").setAttribute("stroke-width", "5");
}

function bookUnHighlight(book) {
    book.getElementById("spine").setAttribute("stroke-width", "0");
}

function bookMove(book, x, y) {
    book.setAttribute("x", x.toString());
    book.setAttribute("y", y.toString());
}

function bookFromInfo(bookInfo) {
    bookInfo.svg = document.createElementNS(svgNamespace, "svg");
    bookInfo.svg.setAttribute("id", "book-" + randString(10));
    bookInfo.svg.setAttribute("x", "0");
    bookInfo.svg.setAttribute("y", "0");
    bookInfo.svg.setAttribute("width", bookInfo.width.toString());
    bookInfo.svg.setAttribute("height", bookInfo.height.toString());
    let bookSpine = document.createElementNS(svgNamespace, "rect");
    bookSpine.setAttribute("id", "spine");
    bookSpine.setAttribute("stroke", "white");
    bookSpine.setAttribute("stroke-width", "0");
    let bookShadow = document.createElementNS(svgNamespace, "rect");
    bookShadow.setAttribute("id", "shadow");
    let bookPaper = document.createElementNS(svgNamespace, "rect");
    bookPaper.setAttribute("id", "paper");
    bookInfo.svg.appendChild(bookSpine);
    bookInfo.svg.appendChild(bookShadow);
    bookInfo.svg.appendChild(bookPaper);
    bookInfo.svg.addEventListener("mouseenter", () => bookHighlight(bookInfo.svg));
    bookInfo.svg.addEventListener("mouseleave", () => bookUnHighlight(bookInfo.svg));
    
    bookLookup[bookInfo.svg.getAttribute("id")] = bookInfo;
    bookSetState(bookInfo.svg, bookInfo.state);
    return bookInfo.svg;
}

function bookCopy(book) {
    let bookInfo = bookGetInfo(book);
    let copyBookInfo = {
        width:      bookInfo.width, 
        height:     bookInfo.height,
        depth:      bookInfo.depth,
        title:      bookInfo.title,
        content:    bookInfo.content,
        state:      bookInfo.state,
        color:      bookInfo.color,
        svg:        undefined
    };
    return bookFromInfo(copyBookInfo);
}

function bookNew(title, content, state = "upright") {
    let width = randRange(24, 60);
    let height = randRange(145, 185);
    let bookInfo = {
        width:  width,
        height: height,
        depth: randRange(height / 2, height * 3 / 4),
        title: title,
        content: content,
        state: state,
        color: bookColors[randRange(0, bookColors.length)],
        svg: undefined
    };
    return bookFromInfo(bookInfo);
}

function bookDelete(book) {
    bookLookup[book.getAttribute("id")] = undefined;
    book.remove();
}

//
//

function bookshelfAdd(book) {
    bookshelfState.push(book);
    bookshelfElem.append(book);
}

function bookshelfGet(index) {
    return bookshelfState[index];
}

function bookshelfLength() {
    return bookshelfState.length;
}

//
//

function tableAdd(book) {
    let tableBook = bookCopy(book);
    let bookInfo = bookGetInfo(tableBook);
    tableState[bookInfo.title] = tableBook;
    tableElem.append(tableBook);
}

function tableGet(title) {
    return tableState[title];
}

function tableRemove(title) {
    let book = tableGet(title);

    if (book !== undefined) {
        bookDelete(book);
    }
}

function tableFocus(title) {
    let book = tableGet(title);
    let bookInfo = bookGetInfo(book);
    if (book !== undefined) {
        bookSetState(book, "open");
        bookMove(book, (700 / 2) - (Number(book.getAttribute("width")) / 2), (200 / 2) - (Number(book.getAttribute("height")) / 2));
    }
}


//
//

async function sleep(timeout) {
    await new Promise((resolve) => setTimeout(resolve, timeout));
}

async function study() {
    for (let i = 0; i != bookshelfLength(); i++) {
        let book = bookshelfGet(i);
        let bookInfo = bookGetInfo(book);
        bookHide(book);

        tableAdd(book);
        await sleep(1000);

        tableFocus(bookInfo.title);
        await sleep(1000);

        bookShow(book);
        tableRemove(bookInfo.title);
        await sleep(1000);
    }
}

//
//

$(document).ready(() => {
    bookshelfElem = $("#bookshelf");    
    tableElem = $("#table");

    $("#study").click(() => study());

    for (let i = 0; i != 16; i++) {
        bookshelfAdd(bookNew(i.toString(), i.toString()));
    }
});