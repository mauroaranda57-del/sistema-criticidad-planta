"""Prueba del sistema completo: 5 consultas que ejercitan RAG, agentes y HITL."""

import asyncio
import time

import httpx

URL_BASE = "http://127.0.0.1:8000"

CONSULTAS = [
    "Analiza la criticidad del compresor C-02 segun su historico del ultimo anio.",
    "Que tareas de mantenimiento preventivo diario indica el manual para la bomba centrifuga?",
    "Que EPP se requiere para intervenir un equipo en planta segun el procedimiento?",
    "Calcula el MTBF y la disponibilidad de la bomba B-07.",
    "Cada cuanto se renueva el EPP de proteccion auditiva segun el procedimiento?",
]


async def esperar_final(cliente: httpx.AsyncClient, job_id: str) -> dict:
    """Hace polling hasta que el job alcanza un estado final."""
    while True:
        await asyncio.sleep(8)
        respuesta = await cliente.get(f"{URL_BASE}/tasks/{job_id}")
        job = respuesta.json()
        if job.get("estado") in ("DONE", "FAILED", "WAITING_APPROVAL"):
            return job


async def main() -> None:
    """Corre las 5 consultas una por una y resume el resultado."""
    inicio_total = time.perf_counter()
    resumen: list[tuple[str, str, float]] = []

    async with httpx.AsyncClient(timeout=30) as cliente:
        for numero, consulta in enumerate(CONSULTAS, start=1):
            print(f"\n--- Prueba {numero}/5 ---")
            print(f"Consulta: {consulta}")

            inicio = time.perf_counter()
            respuesta = await cliente.post(
                f"{URL_BASE}/tasks", json={"consulta": consulta}
            )
            datos = respuesta.json()
            job_id = datos["job_id"]
            latencia_encolado = time.perf_counter() - inicio
            print(f"Encolado como {job_id} en {latencia_encolado:.2f} s")

            job = await esperar_final(cliente, job_id)
            estado = job.get("estado")
            duracion = job.get("duracion_seg", 0)
            print(f"Estado final: {estado} ({duracion} s)")

            if estado == "FAILED":
                print(f"  Error: {job.get('error', '')[:120]}")
            elif estado == "WAITING_APPROVAL":
                print("  El sistema clasifico la tarea como critica y espera aprobacion.")

            resumen.append((job_id, estado, duracion))

    print("\n" + "=" * 70)
    print("RESUMEN DE LAS 5 PRUEBAS")
    print("=" * 70)
    for job_id, estado, duracion in resumen:
        print(f"  {job_id} -> {estado} ({duracion} s)")

    exitosas = sum(1 for _, e, _ in resumen if e in ("DONE", "WAITING_APPROVAL"))
    print(f"\nPruebas completadas sin error: {exitosas}/5")
    print(f"Tiempo total: {time.perf_counter() - inicio_total:.1f} s")
    print("Trazas, costo y latencia disponibles en LangSmith.")


if __name__ == "__main__":
    asyncio.run(main())