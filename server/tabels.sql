
DROP TABLE IF EXISTS Dirs;

CREATE TABLE Dirs (

    dircode CHAR(3),
    dirname VARCHAR(25),
    dirloc CHAR(3),
    PRIMARY KEY (dircode)

);

DROP TABLE IF EXISTS Files;

CREATE TABLE Files (

    id CHAR(3),
    fname VARCHAR(25),
    dircode CHAR(3),
    PRIMARY KEY (id),
    FOREIGN KEY (dircode) REFERENCES Dirs(dircode)

);

INSERT INTO Dirs VALUES ('000','root','000');