/* Single-threaded teaching ring buffer; not ISR-safe or lock-free. */
#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <assert.h>
#include <stdio.h>
#define CAPACITY 4u
struct ring { uint8_t data[CAPACITY]; size_t read, write, count; };
static bool push(struct ring *q, uint8_t v) {
    if (q->count == CAPACITY) return false;
    q->data[q->write] = v;
    q->write = (q->write + 1u) % CAPACITY;
    q->count++;
    return true;
}
static bool pop(struct ring *q, uint8_t *v) {
    if (q->count == 0u) return false;
    *v = q->data[q->read];
    q->read = (q->read + 1u) % CAPACITY;
    q->count--;
    return true;
}
int main(void) {
    struct ring q = {0}; uint8_t v = 0;
    assert(!pop(&q, &v));
    for (uint8_t i = 0; i < CAPACITY; i++) assert(push(&q, i));
    assert(!push(&q, 99));
    assert(pop(&q, &v) && v == 0);
    assert(push(&q, 4));
    for (uint8_t i = 1; i <= CAPACITY; i++) assert(pop(&q, &v) && v == i);
    assert(!pop(&q, &v));
    puts("PASS: empty, full, wraparound, and FIFO ordering");
    return 0;
}
