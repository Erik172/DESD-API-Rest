def is_ip_allowed(ip: str) -> bool:
    """
    Verifica si una dirección IP está permitida según la lista de IPs permitidas almacenadas en la base de datos.
    Args:
        ip (str): La dirección IP que se desea verificar.
    Returns:
        bool: True si la IP está permitida, False en caso contrario.
    La función maneja tanto direcciones IP individuales como rangos de IP en formato CIDR.
    """
    from app.models import AllowedIPs
    
    allowed_ips = AllowedIPs.query.filter_by(is_active=True).all()
    for allowed_ip in allowed_ips:
        if '/' in allowed_ip.ip:
            # Manejar rangos CIDR
            subnet, mask = allowed_ip.ip.split('/')
            mask = int(mask)
            ip_int = int(''.join(f'{int(octet):08b}' for octet in ip.split('.')), 2)
            subnet_int = int(''.join(f'{int(octet):08b}' for octet in subnet.split('.')), 2)
            mask_int = (0xFFFFFFFF << (32 - mask)) & 0xFFFFFFFF
            if (ip_int & mask_int) == (subnet_int & mask_int):
                return True
        else:
            # Manejar IPs individuales
            if ip == allowed_ip.ip:
                return True
    return False