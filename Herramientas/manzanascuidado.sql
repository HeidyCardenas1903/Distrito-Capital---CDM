-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-09-2023 a las 17:21:56
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
-- Estructura de tabla para la tabla `appleservice`
--

CREATE TABLE `appleservice` (
  `copy_codmanzana` int(11) NOT NULL,
  `copy_codservice` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `appleservice`
--

INSERT INTO `appleservice` (`copy_codmanzana`, `copy_codservice`) VALUES
(10789, 1);

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

--
-- Volcado de datos para la tabla `establecimiento`
--

INSERT INTO `establecimiento` (`cod_establecimiento`, `cod_servicio`, `nombre_establecimiento`, `responsable`, `direccion_establecimiento`) VALUES
(32, 5, 'Maria Paquita', 'julian romero', 'calle 54#83-98');

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

--
-- Volcado de datos para la tabla `manzanas`
--

INSERT INTO `manzanas` (`cod_manzana`, `cod_municipio`, `nombre_manzana`, `localidad`, `direccion_manzana`) VALUES
(10789, 5476, 'Morada', 'Resistencia', 'car 65#12-67');

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
  `contraseña` varchar(10) NOT NULL,
  `ciudad` varchar(20) NOT NULL,
  `direccion_mujer` varchar(40) NOT NULL,
  `ocupacion` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mujeres`
--

INSERT INTO `mujeres` (`documento`, `cod_servicio`, `tipoDocumento`, `nombres_mujer`, `apellidos_mujer`, `telefono`, `correo`, `contraseña`, `ciudad`, `direccion_mujer`, `ocupacion`) VALUES
(1019132790, 2, 'CC', 'Vivian', 'hincapie', '3194091311', 'carohinca1997@gmail.com', 'caro12345', 'Bogotá', 'calle 168a # 73 a-96', 'Desarrolladora'),
(1020816856, 5, 'TI', 'juana', 'jimenez', '3158344617', 'juana@gmail.com', '123456juan', 'medellin', 'calle siempre viva', 'medico');

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
(3344, 'Antioquia'),
(5476, 'Nariño');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `cod_servicio` int(11) NOT NULL,
  `nombre_servicio` varchar(40) NOT NULL,
  `descripcion` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`cod_servicio`, `nombre_servicio`, `descripcion`) VALUES
(1, 'Estudiar', 'Servicio que presta ayuda para la educación'),
(2, 'Emprender', 'Servicio que presta ayuda a las mujeres que quieren ser sus propias jefas'),
(3, 'Emplearse', 'Servicio que busca ayudar a las mujeres que buscan emplearse'),
(4, 'Descansar', 'Buscando la comodidad y descanso apropiado de todas las mujeres trabajadoras o d'),
(5, 'Ejercitarse', 'Con el fin de buscar una salud física idónea para todas las mujeres'),
(6, 'Recibir Orientación', 'Servicio dedicado a a la ayuda de mujeres que deben tomar decisiones importantes'),
(7, 'Asesoria Juridica', 'Con el fin de que todas las mujeres tengas una representacion legal'),
(8, 'Asesoria Psicologica', 'La salud mental es lo primordial, acceso a todas las mujeres'),
(9, 'Lavanderias Comunitarias', 'Con el fin de ayudar a las mujeres que no puedan completar esta labor de casa en');

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
-- Indices de la tabla `appleservice`
--
ALTER TABLE `appleservice`
  ADD PRIMARY KEY (`copy_codmanzana`,`copy_codservice`),
  ADD KEY `copy_codservice` (`copy_codservice`);

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
-- Filtros para la tabla `appleservice`
--
ALTER TABLE `appleservice`
  ADD CONSTRAINT `appleservice_ibfk_1` FOREIGN KEY (`copy_codmanzana`) REFERENCES `manzanas` (`cod_manzana`),
  ADD CONSTRAINT `appleservice_ibfk_2` FOREIGN KEY (`copy_codservice`) REFERENCES `servicios` (`cod_servicio`);

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
-- Filtros para la tabla `mujeres`
--
ALTER TABLE `mujeres`
  ADD CONSTRAINT `mujeres_ibfk_1` FOREIGN KEY (`cod_servicio`) REFERENCES `servicios` (`cod_servicio`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
