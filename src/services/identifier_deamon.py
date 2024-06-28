import time
from src.services.raw_frame_service import RawFrameService
from src.models.sightingModel import Sighting
from src.models.frameModel import Frame
from src.util.database.db import db
import logging
class IdentifierDaemon:
    def __init__(self):
        self.running = True
        self.raw_frame_service = RawFrameService()

    def validate_sightings(self, sightings_data):
        for data in sightings_data:
            if not data.get('pixels_area') or not data.get('individual'):
                return False
        return True
    
    def run(self, capture_time=1):
        while self.running:
            raw_frame = self.raw_frame_service.capture_frame(0)
            #TODO: Logica para pasar al servicio de sightings y si lo que regresa tiene un individual persistir
            #data de ejemplo: 
            sightings_data = [
                {'pixel_area': b'\x00\x01\x02\x03', 'individual': 124},
                {'pixel_area': b'\x00\x01\x02\x03' , 'individual': 124515}
            ]
            if not self.validate_sightings(sightings_data=sightings_data):
                time.sleep(capture_time)
                continue
            with db.session() as session:
                try:
                    session.add(raw_frame)
                    session.commit()
                    #Recorre el conjunto de sightings para persistirlos 
                    for sighting_data in sightings_data:
                        sighting = Sighting(
                            pixel_area=sighting_data['pixel_area'],
                            individual=sighting_data['individual'],
                            raw_frame_id=raw_frame.id
                        )
                        session.add(sighting)
                        session.commit()

                        frame = Frame(
                            raw_frame_id=raw_frame.id,
                            sighting_id=sighting.id
                        )
                        session.add(frame)
                        session.commit()

                except Exception as e:
                    session.rollback()
                    print(f"Error: {e}")