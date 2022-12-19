-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Dec 12, 2022 at 07:27 PM
-- Server version: 8.0.31
-- PHP Version: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `CargooDB`
--
CREATE DATABASE IF NOT EXISTS `CargooDB` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci;
USE `CargooDB`;

-- --------------------------------------------------------

--
-- Stand-in structure for view `nodeControl`
-- (See below for the actual view)
--
CREATE TABLE `nodeControl` (
`BoxID` int
,`BoxStatus` int
,`destNodeID` int
,`NodeID` int
);

-- --------------------------------------------------------

--
-- Table structure for table `tblBoxes`
--

CREATE TABLE `tblBoxes` (
  `ID` int NOT NULL,
  `NodeID` int NOT NULL,
  `BoxID` int NOT NULL,
  `BoxStatus` int NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Dumping data for table `tblBoxes`
--

INSERT INTO `tblBoxes` (`ID`, `NodeID`, `BoxID`, `BoxStatus`) VALUES
(1, 3, 1, 1),
(3, 3, 2, 1),
(4, 3, 3, 0),
(5, 4, 1, 1),
(6, 4, 2, 1),
(7, 4, 3, 0),
(8, 5, 1, 1),
(9, 5, 2, 0),
(10, 6, 1, 0),
(11, 6, 2, 0),
(12, 6, 3, 0),
(13, 6, 4, 0),
(14, 7, 1, 0),
(15, 7, 2, 0),
(16, 7, 3, 0),
(17, 8, 1, 0),
(18, 8, 2, 0),
(19, 8, 3, 0),
(20, 9, 1, 0),
(21, 9, 2, 0),
(22, 9, 3, 0),
(23, 10, 1, 0),
(24, 10, 2, 0),
(25, 10, 3, 0),
(26, 11, 1, 0),
(27, 11, 2, 0),
(28, 11, 3, 0),
(29, 20, 1, 0),
(30, 20, 2, 0),
(31, 20, 3, 0),
(32, 20, 4, 0);

-- --------------------------------------------------------

--
-- Table structure for table `tblCargo`
--

CREATE TABLE `tblCargo` (
  `ID` int NOT NULL,
  `OwnerID` int NOT NULL,
  `DriverID` int DEFAULT '0',
  `ReceiverID` int DEFAULT '0',
  `Type` varchar(25) COLLATE utf8mb4_turkish_ci NOT NULL,
  `Weight` double NOT NULL,
  `Volume` double NOT NULL,
  `NodeID` int DEFAULT NULL,
  `destNodeID` int NOT NULL DEFAULT '0',
  `BoxID` int NOT NULL DEFAULT '1',
  `BoxStatus` int NOT NULL DEFAULT '0',
  `Status` varchar(25) COLLATE utf8mb4_turkish_ci NOT NULL,
  `DateCargo` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Value` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Dumping data for table `tblCargo`
--

INSERT INTO `tblCargo` (`ID`, `OwnerID`, `DriverID`, `ReceiverID`, `Type`, `Weight`, `Volume`, `NodeID`, `destNodeID`, `BoxID`, `BoxStatus`, `Status`, `DateCargo`, `Value`) VALUES
(23, 55, 0, 72, 'food', 22, 15, 3, 20, 2, 2, 'startbox', '2022-12-03 15:59:04', 100),
(24, 72, 0, 2, 'food', 22, 15, 3, 20, 3, 2, 'startbox', '2022-12-03 15:59:07', 55),
(34, 72, 0, 55, 'food', 22, 15, 5, 20, 1, 0, 'startbox', '2022-12-08 10:57:11', 145),
(35, 72, 0, 0, 'food', 22, 15, 4, 20, 1, 0, 'startbox', '2022-12-08 11:08:11', 130),
(36, 72, 0, 62, 'Food', 335, 15, 3, 8, 3, 2, 'startbox', '2022-12-09 10:33:36', 33515),
(37, 72, 0, 72, 'Clothes', 44, 333, 5, 3, 1, 2, 'done', '2022-12-09 10:53:21', 44333),
(38, 72, 0, 72, 'Clothes', 21, 123, 3, 20, 1, 2, 'startbox', '2022-12-09 12:01:00', 21123);

-- --------------------------------------------------------

--
-- Table structure for table `tblNode`
--

CREATE TABLE `tblNode` (
  `ID` int NOT NULL,
  `nodeName` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `latitude` float NOT NULL,
  `longitude` double(35,10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Dumping data for table `tblNode`
--

INSERT INTO `tblNode` (`ID`, `nodeName`, `latitude`, `longitude`) VALUES
(1, 's', 40, 33.0000000000),
(2, 'q', 39.9255, 32.8662870000),
(3, 'Bostanlı iskele', 38.4544, 27.0966848000),
(4, 'Karşıyaka iskele', 38.4552, 27.1199392504),
(5, 'Bayraklı izban', 38.4638, 27.1642137201),
(6, 'Forum Bornova', 38.4492, 27.2093774134),
(7, 'Alsancak izban', 38.4393, 27.1478358578),
(8, 'Konak Metro', 38.4177, 27.1281828997),
(9, '9 Eylül üniversitesi ', 38.3701, 27.2062576759),
(10, 'Agora AVM', 38.3944, 27.0532809185),
(11, 'Magnesia AVM', 38.6158, 27.4003039302),
(20, 'Manisa Celal Bayar üni', 38.6753, 27.3088680784);

-- --------------------------------------------------------

--
-- Table structure for table `tblUser`
--

CREATE TABLE `tblUser` (
  `ID` int NOT NULL,
  `NationalID` text CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `Mail` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `Password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `Name` varchar(25) COLLATE utf8mb4_turkish_ci NOT NULL,
  `LastName` varchar(25) COLLATE utf8mb4_turkish_ci NOT NULL,
  `Phone` text CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `Adress` text CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci NOT NULL,
  `Balance` double NOT NULL,
  `Star` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_turkish_ci;

--
-- Dumping data for table `tblUser`
--

INSERT INTO `tblUser` (`ID`, `NationalID`, `Mail`, `Password`, `Name`, `LastName`, `Phone`, `Adress`, `Balance`, `Star`) VALUES
(22, '161651', 'mail1', '3I6pIcnsZobLkXctF+Glsg==', 'tanyeli', '6060', '41561651', 'dfsddsf', 0, 0),
(23, '45458', 'mail2', '1234', 'ismai', 'tosun', '5456487', 'dasdas', 0, 0),
(34, '45458', 'mail3', '1234', 'ismai', 'tosun', '5456487', 'dasdas', 0, 0),
(42, '2255', 'Tanyeli6060@mail', '3I6pIcnsZobLkXctF+Glsg==', 'ismail', 'tanyeli', '0535', 'Tokat', 0, 0),
(45, '2255', 'Tanyeli6060@mails', '3I6pIcnsZobLkXctF+Glsg==', 'ismail', 'tanyeli', '0535', 'Tokat', 0, 0),
(46, '2255', 'Tanyeli6060@mailss', '3I6pIcnsZobLkXctF+Glsg==', 'ismail', 'tanyeli', '0535', 'Tokat', 0, 0),
(47, '2255', 'Tanyeli6060@mailsss', '3I6pIcnsZobLkXctF+Glsg==', 'ismail', 'tanyeli', '0535', 'Tokat', 0, 0),
(52, '2255', 'aaaaa', 'NSpJF4mGsyDe8/cpqPKocg==', 'ismail', 'tanyeli', 'Tokat', '0535', 0, 0),
(62, '444', 'aa', 'MVeSXkuisFJn2sG/KYzlDQ==', 'sadasd', 'asdsad', 'ddd', '444', 0, 0),
(64, '5616', '1234', 'uS5+blKoRYWDDI832SsZrQ==', 'nw', 'nw', 'sadsad', '65456', 0, 0),
(72, '232132', 'mail60', 'gi1/yl28BYqknJ7GFXy++g==', 'ismail', 'TOSUN', '56456', 'izzmir', 600, 0),
(73, '55', 'er', 'gi1/yl28BYqknJ7GFXy++g==', 'sda', 'sad', '4', 'a', 0, 0),
(100, '1000', 'zafer@gmail.com', '1234', 'Zafer', 'Say', '5427767522', 'izmir', 500, 10);

-- --------------------------------------------------------

--
-- Stand-in structure for view `viewNodeCargo`
-- (See below for the actual view)
--
CREATE TABLE `viewNodeCargo` (
`cargo_ID` int
,`DateCargo` timestamp
,`DriverID` int
,`latitude` float
,`longitude` double(35,10)
,`node_ID` int
,`nodeName` varchar(30)
,`OwnerID` int
,`ReceiverID` int
,`Status` varchar(25)
,`Type` varchar(25)
,`Value` double
,`Volume` double
,`Weight` double
);

-- --------------------------------------------------------

--
-- Structure for view `nodeControl`
--
DROP TABLE IF EXISTS `nodeControl`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `nodeControl`  AS SELECT `tblCargo`.`NodeID` AS `NodeID`, `tblCargo`.`destNodeID` AS `destNodeID`, `tblCargo`.`BoxID` AS `BoxID`, `tblCargo`.`BoxStatus` AS `BoxStatus` FROM `tblCargo``tblCargo`  ;

-- --------------------------------------------------------

--
-- Structure for view `viewNodeCargo`
--
DROP TABLE IF EXISTS `viewNodeCargo`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `viewNodeCargo`  AS SELECT `tblCargo`.`ID` AS `cargo_ID`, `tblNode`.`ID` AS `node_ID`, `tblNode`.`nodeName` AS `nodeName`, `tblNode`.`latitude` AS `latitude`, `tblNode`.`longitude` AS `longitude`, `tblCargo`.`OwnerID` AS `OwnerID`, `tblCargo`.`DriverID` AS `DriverID`, `tblCargo`.`ReceiverID` AS `ReceiverID`, `tblCargo`.`Type` AS `Type`, `tblCargo`.`Weight` AS `Weight`, `tblCargo`.`Volume` AS `Volume`, `tblCargo`.`Status` AS `Status`, `tblCargo`.`DateCargo` AS `DateCargo`, `tblCargo`.`Value` AS `Value` FROM (`tblNode` join `tblCargo` on((`tblNode`.`ID` = `tblCargo`.`NodeID`)))  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tblBoxes`
--
ALTER TABLE `tblBoxes`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `tblCargo`
--
ALTER TABLE `tblCargo`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `tblNode`
--
ALTER TABLE `tblNode`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `tblUser`
--
ALTER TABLE `tblUser`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Mail` (`Mail`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tblBoxes`
--
ALTER TABLE `tblBoxes`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `tblCargo`
--
ALTER TABLE `tblCargo`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `tblNode`
--
ALTER TABLE `tblNode`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `tblUser`
--
ALTER TABLE `tblUser`
  MODIFY `ID` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=101;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
