CREATE TABLE `Diagnose` (
  `P_ID` varchar(20) NOT NULL,
  `C_ID` varchar(20) NOT NULL,
  `LoggedDate` datetime NOT NULL,
  `End_Date` datetime DEFAULT NULL,
  `Degree_of_Severity` varchar(30) DEFAULT NULL,
  KEY `P_ID` (`P_ID`),
  KEY `C_ID` (`C_ID`),
  CONSTRAINT `Diagnose_ibfk_1` FOREIGN KEY (`P_ID`) REFERENCES `Persons` (`PersonID`),
  CONSTRAINT `Diagnose_ibfk_2` FOREIGN KEY (`C_ID`) REFERENCES `Health_Condition` (`Condition_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `EYES` (
  `P_ID` varchar(20) NOT NULL,
  `LoggedDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Iris_R` varchar(20) DEFAULT NULL,
  `Iris_L` varchar(20) DEFAULT NULL,
  `Sclera` varchar(20) DEFAULT NULL,
  `Depth_Perception` int DEFAULT NULL,
  `Mobility` int DEFAULT NULL,
  `Notes` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`P_ID`,`LoggedDate`),
  CONSTRAINT `EYES_ibfk_1` FOREIGN KEY (`P_ID`) REFERENCES `Persons` (`PersonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
CREATE TABLE `Growth` (
  `P_ID` varchar(20) NOT NULL,
  `LoggedDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Height` float NOT NULL,
  `Weight` float NOT NULL,
  `HealthHabbit` varchar(1000) DEFAULT NULL,
  `Note` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`P_ID`,`LoggedDate`),
  CONSTRAINT `Growth_ibfk_1` FOREIGN KEY (`P_ID`) REFERENCES `Persons` (`PersonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Gums` (
  `P_ID` varchar(20) NOT NULL,
  `LoggedDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Hyperplasia` tinyint(1) DEFAULT '0',
  `Gingivitis` tinyint(1) DEFAULT '0',
  `Periodontitis` tinyint(1) DEFAULT '0',
  `Pocket_depths` float DEFAULT NULL,
  `Mobility` float DEFAULT NULL,
  PRIMARY KEY (`P_ID`,`LoggedDate`),
  CONSTRAINT `Gums_ibfk_1` FOREIGN KEY (`P_ID`, `LoggedDate`) REFERENCES `dental_record` (`P_ID`, `LoggedDate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Has_Mutation` (
  `P_ID` varchar(20) NOT NULL,
  `Gene` varchar(20) NOT NULL,
  `Note` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`P_ID`,`Gene`),
  CONSTRAINT `Has_Mutation_ibfk_1` FOREIGN KEY (`P_ID`) REFERENCES `Persons` (`PersonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Health_Condition` (
  `Condition_ID` varchar(10) NOT NULL,
  `Name` varchar(40) NOT NULL,
  `Type` varchar(40) NOT NULL,
  `Acronym` varchar(12) DEFAULT NULL,
  PRIMARY KEY (`Condition_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Persons` (
  `PersonID` varchar(20) NOT NULL,
  `Date_of_birth` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Sex` varchar(4) NOT NULL DEFAULT 'XX',
  `Orthodontic_treatment` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`PersonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tooth` (
  `P_ID` varchar(20) NOT NULL,
  `LoggedDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Tooth` varchar(20) NOT NULL,
  `Side` varchar(20) NOT NULL,
  `Position` varchar(20) NOT NULL DEFAULT 'First',
  `Upper` tinyint(1) NOT NULL DEFAULT '0',
  `Secondary` tinyint(1) NOT NULL DEFAULT '1',
  `Missing` tinyint(1) NOT NULL DEFAULT '0',
  `Size` varchar(20) DEFAULT 'Normal',
  `Color` varchar(20) DEFAULT NULL,
  `Eruption` int DEFAULT NULL,
  `Caries` tinyint(1) DEFAULT '0',
  `Occlusal_wear` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`P_ID`,`LoggedDate`,`Tooth`,`Side`,`Position`,`Upper`,`Secondary`),
  CONSTRAINT `Tooth_ibfk_1` FOREIGN KEY (`P_ID`, `LoggedDate`) REFERENCES `dental_record` (`P_ID`, `LoggedDate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clinical_notes` (
  `PID` varchar(20) NOT NULL,
  `LoggedDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Drug` varchar(20) DEFAULT NULL,
  `Strength` varchar(40) DEFAULT NULL,
  `Duration` varchar(20) DEFAULT NULL,
  `Route` varchar(20) DEFAULT NULL,
  `Form` varchar(20) DEFAULT NULL,
  `ADE` varchar(20) DEFAULT NULL,
  `Dosage` varchar(20) DEFAULT NULL,
  `Reason` varchar(40) DEFAULT NULL,
  `Frequency` varchar(20) DEFAULT NULL,
  `Note` varchar(255) NOT NULL,
  `Entry_ID` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Entry_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dental_record` (
  `P_ID` varchar(20) NOT NULL,
  `LoggedDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Num_Teeth` int NOT NULL,
  `Dentition_stage` varchar(20) DEFAULT 'permanent',
  `Erupt_rate` varchar(20) DEFAULT 'normal',
  `Occlusion` varchar(20) DEFAULT 'normal',
  `Tooth_color` varchar(20) DEFAULT 'normal',
  `Oral_hygiene` varchar(20) DEFAULT 'good',
  `TMJ` tinyint(1) NOT NULL DEFAULT '0',
  `Note` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`P_ID`,`LoggedDate`),
  CONSTRAINT `dental_record_ibfk_1` FOREIGN KEY (`P_ID`) REFERENCES `Persons` (`PersonID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
