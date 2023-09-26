-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-09-2023 a las 00:37:54
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `manzanascuidado`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cuidadoras`
--

CREATE TABLE `cuidadoras` (
  `documento_mujer` int(11) NOT NULL,
  `cod_manzana` int(11) NOT NULL,
  `cod_servicio` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `establecimiento`
--

CREATE TABLE `establecimiento` (
  `cod_establecimiento` int(11) NOT NULL,
  `cod_servicio` int(11) NOT NULL,
  `nombre_establecimiento` varchar(40) NOT NULL,
  `responsable` varchar(40) NOT NULL,
  `direccion_establecimiento` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `manzanas`
--

CREATE TABLE `manzanas` (
  `cod_manzana` int(11) NOT NULL,
  `cod_municipio` int(11) NOT NULL,
  `nombre_manzana` varchar(40) NOT NULL,
  `localidad` varchar(40) NOT NULL,
  `direccion_manzana` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `manzanas_servicios`
--

CREATE TABLE `manzanas_servicios` (
  `cod_manzana` int(11) NOT NULL,
  `cod_servicio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mujeres`
--

CREATE TABLE `mujeres` (
  `documento` int(11) NOT NULL,
  `cod_servicio` int(11) NOT NULL,
  `tipoDocumento` enum('CC','TI','Pasaporte','CE') NOT NULL,
  `nombres_mujer` varchar(40) NOT NULL,
  `apellidos_mujer` varchar(40) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `correo` varchar(40) NOT NULL,
  `ciudad` varchar(20) NOT NULL,
  `direccion_mujer` varchar(40) NOT NULL,
  `ocupacion` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `municipios`
--

CREATE TABLE `municipios` (
  `cod_municipio` int(11) NOT NULL,
  `nombre_municipio` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `municipios`
--

INSERT INTO `municipios` (`cod_municipio`, `nombre_municipio`) VALUES
(3344, 'Cundiinamarca'),
(3456, 'Antioquia');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `cod_servicio` int(11) NOT NULL,
  `nombre_servicio` varchar(40) NOT NULL,
  `descripcion` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `cod_usuario` int(11) NOT NULL,
  `nombre` varchar(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `contraseña` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`cod_usuario`, `nombre`, `email`, `contraseña`) VALUES
(1, 'Juan', 'juan@gmail.com', 'juan123456');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cuidadoras`
--
ALTER TABLE `cuidadoras`
  ADD PRIMARY KEY (`documento_mujer`,`cod_manzana`,`cod_servicio`),
  ADD KEY `cod_manzana` (`cod_manzana`),
  ADD KEY `cod_servicio` (`cod_servicio`);

--
-- Indices de la tabla `establecimiento`
--
ALTER TABLE `establecimiento`
  ADD PRIMARY KEY (`cod_establecimiento`),
  ADD KEY `cod_servicio` (`cod_servicio`);

--
-- Indices de la tabla `manzanas`
--
ALTER TABLE `manzanas`
  ADD PRIMARY KEY (`cod_manzana`),
  ADD KEY `cod_municipio` (`cod_municipio`);

--
-- Indices de la tabla `manzanas_servicios`
--
ALTER TABLE `manzanas_servicios`
  ADD PRIMARY KEY (`cod_manzana`,`cod_servicio`),
  ADD KEY `cod_servicio` (`cod_servicio`);

--
-- Indices de la tabla `mujeres`
--
ALTER TABLE `mujeres`
  ADD PRIMARY KEY (`documento`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `cod_servicio` (`cod_servicio`);

--
-- Indices de la tabla `municipios`
--
ALTER TABLE `municipios`
  ADD PRIMARY KEY (`cod_municipio`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`cod_servicio`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`cod_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cuidadoras`
--
ALTER TABLE `cuidadoras`
  ADD CONSTRAINT `cuidadoras_ibfk_1` FOREIGN KEY (`documento_mujer`) REFERENCES `mujeres` (`documento`),
  ADD CONSTRAINT `cuidadoras_ibfk_2` FOREIGN KEY (`cod_manzana`) REFERENCES `manzanas` (`cod_manzana`),
  ADD CONSTRAINT `cuidadoras_ibfk_3` FOREIGN KEY (`cod_servicio`) REFERENCES `servicios` (`cod_servicio`);

--
-- Filtros para la tabla `establecimiento`
--
ALTER TABLE `establecimiento`
  ADD CONSTRAINT `establecimiento_ibfk_1` FOREIGN KEY (`cod_servicio`) REFERENCES `servicios` (`cod_servicio`);

--
-- Filtros para la tabla `manzanas`
--
ALTER TABLE `manzanas`
  ADD CONSTRAINT `manzanas_ibfk_1` FOREIGN KEY (`cod_municipio`) REFERENCES `municipios` (`cod_municipio`);

--
-- Filtros para la tabla `manzanas_servicios`
--
ALTER TABLE `manzanas_servicios`
  ADD CONSTRAINT `manzanas_servicios_ibfk_1` FOREIGN KEY (`cod_manzana`) REFERENCES `manzanas` (`cod_manzana`),
  ADD CONSTRAINT `manzanas_servicios_ibfk_2` FOREIGN KEY (`cod_servicio`) REFERENCES `servicios` (`cod_servicio`);

--
-- Filtros para la tabla `mujeres`
--
ALTER TABLE `mujeres`
  ADD CONSTRAINT `mujeres_ibfk_1` FOREIGN KEY (`cod_servicio`) REFERENCES `servicios` (`cod_servicio`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
