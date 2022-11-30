# -*- coding: utf-8 -*- 
#----------------------------------------------------------------------------
# Creado por: Pedro Pablo Arriola Jimenez (20188)   
# Fecha de creación: 30/11/2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" Proyecto 3: Raycaster that lets you play CASTLE WOLFENSTEIN""" 
# ---------------------------------------------------------------------------

from raycast import Raycaster

wolfenstein_raycast = Raycaster()
wolfenstein_raycast.load_map('./level/map.txt')
wolfenstein_raycast.start_game()