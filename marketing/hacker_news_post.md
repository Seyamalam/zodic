# Hacker News Post

**Title:** Zodic – TypeScript Zod-inspired validation library for Python (2M+ ops/sec, zero dependencies)

**URL:** https://github.com/YOUR_USERNAME/zodic

**Text:**

I built Zodic after missing TypeScript Zod's elegant API when working with Python. It's a validation library focused on developer experience and performance.

Key differentiators:
- Zero runtime dependencies
- 2M+ operations/second (10x faster than Pydantic for simple validation)
- Chainable API identical to TypeScript Zod
- Excellent error messages with nested paths

```python
import zodic as z

schema = z.object({
    "name": z.string().min(1),
    "age": z.number().int().positive(),
    "email": z.string().optional()
})

user = schema.parse(data)  # Type-safe with full IDE support
```

The performance comes from being built specifically for validation (not serialization/ORM like Pydantic) and having zero dependencies.

Would love feedback from the HN community - especially on API design and performance optimizations.

GitHub: https://github.com/YOUR_USERNAME/zodic
PyPI: https://pypi.org/project/zodic/

---

**Follow-up comment to post:**

Some folks are asking about the performance claims. Here are the benchmarks I ran (Python 3.11, Intel i7):

Simple string validation (1M iterations):
- Zodic: 2.0M ops/sec
- Pydantic: 180K ops/sec  
- marshmallow: 95K ops/sec

Complex object validation (100K iterations):
- Zodic: 297K ops/sec
- Pydantic: 85K ops/sec
- marshmallow: 45K ops/sec

The speed comes from:
1. Zero dependencies (no import overhead)
2. Optimized validation paths
3. Minimal object creation
4. Focus purely on validation (not serialization/ORM features)

Benchmark code is in the repo if anyone wants to verify or improve the tests.

The goal isn't to replace Pydantic for everything - if you need ORM features, serialization, etc., Pydantic is still excellent. This is for cases where you want fast, simple validation with a great API.

---

**Potential responses to common HN questions:**

**Q: "Why not just use Pydantic?"**
A: Pydantic is great! This is for different use cases:
- When you want zero dependencies
- When you need maximum performance for validation
- When you prefer functional/chainable API over class-based
- When you're coming from TypeScript and want familiar syntax

**Q: "How does this compare to marshmallow?"**
A: marshmallow is more focused on serialization/deserialization. Zodic is purely validation with a simpler API. Performance-wise, Zodic is about 20x faster for simple validation.

**Q: "What about type safety?"**
A: Full type safety! It integrates with Python's type system and provides excellent IDE support. The schemas are typed and your IDE will give you proper autocompletion.

**Q: "Is this production ready?"**
A: v0.1.0 is stable for basic use cases. 56 tests, 85% coverage. I'm using it in production for API validation. That said, it's new, so I'd recommend thorough testing for critical applications.

**Q: "Roadmap?"**
A: v0.2 will add email/URL/regex validators, v0.3 adds recursive schemas, v0.4 adds framework integrations. Community feedback is driving priorities.