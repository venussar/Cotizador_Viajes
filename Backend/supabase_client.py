from supabase import create_client #se crea conexion con supabase
import os #interactuar con las variables del entorno

SUPABASE_URL = "https://dmholvycvbulwmcpuqqz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRtaG9sdnljdmJ1bHdtY3B1cXF6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA2NjY0NzksImV4cCI6MjA4NjI0MjQ3OX0.WGLUKjiZXmyxQo5nT77GZJQuYnTBsELNUl2JrBs34kk"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY) #se crea la conexion con supabase
