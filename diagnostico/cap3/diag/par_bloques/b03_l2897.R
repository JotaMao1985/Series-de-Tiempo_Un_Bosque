# Raices de phi(B) = 1 - phi1*B - phi2*B^2
# polyroot() recibe los coeficientes en orden ASCENDENTE de potencia
phi <- c(1.4, -0.75)
raices <- polyroot(c(1, -phi))
raices
#> [1] 0.9333333+0.6798693i 0.9333333-0.6798693i   (complejas conjugadas)

Mod(raices)          # modulo: debe ser > 1 para que sea estacionario
#> [1] 1.154701 1.154701
all(Mod(raices) > 1) # veredicto
#> [1] TRUE

# Un caso NO estacionario: phi = 1 es la caminata aleatoria
Mod(polyroot(c(1, -1)))
#> [1] 1            (justo sobre el circulo: raiz unitaria)