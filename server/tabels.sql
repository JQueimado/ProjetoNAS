
DROP TABLE IF EXISTS Files;
DROP TABLE IF EXISTS Dirs;

CREATE TABLE Dirs (

    dircode CHAR(3),
    dirname VARCHAR(25),
    dirloc CHAR(3),
    PRIMARY KEY (dircode)

);

CREATE TABLE Files (

    id CHAR(3),
    fname VARCHAR(25),
    floc CHAR(3),
    PRIMARY KEY (id)

);

INSERT INTO Dirs VALUES ('000','root','000');
INSERT INTO Dirs VALUES ('001','trash','000');